import param
import numpy as np
import pandas as pd
from pandas import Index
from pandas.plotting.base import FramePlotMethods, SeriesPlotMethods, \
                                 register_engine
import holoviews as hv
from holoviews.core.util import datetime_types, unicode


class HoloViewsConverter(param.Parameterized):
    _attr_defaults = {'logy': False, 'logx': False, 'loglog': False,
                      'mark_right': True, 'stacked': False}

    def __init__(self, data, kind=None, by=None, subplots=False, sharex=True,
                 sharey=True, use_index=True,
                 figsize=None, grid=False, legend=True, rot=None,
                 ax=None, fig=None, title=None, xlim=None, ylim=None,
                 xticks=None, yticks=None, sort_columns=False, fontsize=None,
                 secondary_y=False, colormap=None, stacked=False,
                 table=False, layout=None, logx=False, logy=False, **kwds):

        self.data = data
        self.sort_columns = sort_columns
        self.figsize = figsize
        self.layout = layout

        if 'cmap' in kwds and colormap:
            raise TypeError("Only specify one of `cmap` and `colormap`.")
        elif 'cmap' in kwds:
            cmap = kwds.pop('cmap')
        else:
            cmap = colormap

        # Cannot be easily controlled currently
        shared_axes = (sharex and sharey)

        self._plot_opts = {'xticks': xticks, 'yticks': yticks,
                           'yrotation': rot, 'xrotation': rot,
                           'show_grid': grid, 'logx': logx,
                           'logy': logy, 'shared_axes': shared_axes,
                           'show_legend': legend}
        self._element_params = {'label': title}
        self._dim_ranges = {'x': xlim, 'y': ylim}
        self._style_opts = {'fontsize': fontsize, 'cmap': cmap}

        self.stacked = stacked
        self.table = table
        self.use_index = use_index

        # Ignore for now
        self.ax = ax
        self.fig = fig
        self.axes = None
        self.subplots = subplots

        self.legend = legend
        self.legend_handles = []
        self.legend_labels = []

        # parse errorbar input if given
        xerr = kwds.pop('xerr', None)
        yerr = kwds.pop('yerr', None)
        self.errors = {}
        #for kw, err in zip(['xerr', 'yerr'], [xerr, yerr]):
        #    self.errors[kw] = self._parse_errorbars(kw, err)
        self.secondary_y = secondary_y
        self.kwds = kwds


class HoloViewsFrameConverter(HoloViewsConverter):
    def __call__(self, kind, x, y):
        return getattr(self, kind)(x, y)

    def line(self, x, y):
        if x and y:
            return hv.Curve(self.data, kdims=[x], vdims=[y])
        else:
            df = self.data
            x = df.index.name or 'index'
            cols = df.columns
            df = df.reset_index()
            curves = {}
            for c in cols:
                curves[c] = hv.Curve(df, kdims=[x], vdims=[c]).opts(plot=self._plot_opts)
            return hv.NdOverlay(curves)

    def bar(self, x, y):
        if x and y:
            return hv.Bars(self.data, kdims=[x], vdims=[y]).opts(plot=self._plot_opts)
        index = self.data.index.name or 'index'
        df = self.data.reset_index()
        df = pd.melt(df, id_vars=[index], var_name='Group', value_name='Value')
        plot_opts = dict(self._plot_opts)
        plot_opts['stack_index'] = 1 if self.stacked else None
        return hv.Bars(df, kdims=[index, 'Group'], vdims=['Value']).opts(plot=plot_opts)

    def box(self, x, y):
        if x and y:
            return hv.BoxWhisker(self.data, kdims=[x], vdims=[y]).opts(plot=self._plot_opts)
        index = self.data.index.name or 'index'
        df = self.data.reset_index()
        df = pd.melt(df, id_vars=[index], var_name='Group', value_name='Value')
        plot_opts = dict(self._plot_opts)
        plot_opts['invert_axes'] = not self.kwds.get('vert', True)
        return hv.BoxWhisker(df, kdims=['Group'], vdims=['Value']).opts(plot=plot_opts)

    def barh(self, x, y):
        self._plot_opts['invert_axes'] = True
        return self.bar(x, y)

    def hist(self, x, y):
        hists = {}
        ds = hv.Dataset(self.data)
        plot_opts = dict(self._plot_opts)
        plot_opts['invert_axes'] = self.kwds.get('orientation', False) == 'horizontal'
        opts = dict(plot=plot_opts, style=dict(alpha=self.kwds.get('alpha', 1)))
        for col in self.data.columns:
            hists[col] = hv.operation.histogram(ds, dimension=col).opts(**opts)
        return hv.NdOverlay(hists)

    def area(self, x, y):
        if x and y:
            return hv.Area(self.data, kdims=[x], vdims=[y]).opts(plot=self._plot_opts)
        index = self.data.index.name or 'index'
        df = self.data.reset_index()
        areas = []
        for c in self.data.columns:
            areas.append(hv.Area(df, kdims=[index], vdims=[c], label=c))
        areas = hv.Overlay(areas)
        if self.stacked:
            return hv.Area.stack(areas)
        else:
            return areas

    def scatter(self, x, y):
        df = self.data
        vdims = [y]
        style, plot = {}, dict(self._plot_opts)
        if 'color' in self.kwds:
            style['color'] = self.kwds['color']
        if self.kwds.get('c') is not None:
            plot['color_index'] = self.kwds['c']
            plot['colorbar'] = True
            vdims.append(self.kwds['c'])
        if self.kwds.get('s') is not None:
            s = np.sqrt(self.kwds['s'])
            if np.isscalar(s):
                style['size'] = s
            else:
                df['size_var'] = s
                plot['size_index'] = 'size_var'
                vdims.append('size_var')
        opts = dict(style=style, plot=plot)
        label = self.kwds.get('label', '')
        if x and y:
            return hv.Scatter(df, kdims=[x], vdims=vdims, label=label).opts(**opts)




register_engine("holoviews", 'series', HoloViewsSeriesPlotMethods)
register_engine("holoviews", 'frame', HoloViewsFramePlotMethods)
