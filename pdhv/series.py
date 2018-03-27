import param
import holoviews as hv
from holoviews.core.util import datetime_types, unicode


class HoloViewsSeriesConverter(HoloViewsConverter):
    def __call__(self, kind):
        return getattr(self, kind)()

    def bar(self):
        df = self.data.reset_index()
        x, y = df.columns
        label = ''
        if isinstance(y, datetime_types):
            label = unicode(y)
            df = df.rename(columns={y: 'Value'})
            y = 'Value'
        return hv.Bars(df,
                       kdims=[x],
                       vdims=[y],
                       label=label).opts(plot=self._plot_opts)

    def barh(self):
        self._plot_opts['invert_axes'] = True
        return self.bar()

    def hist(self):
        ds = hv.Dataset(self.data.to_frame())
        plot_opts = dict(self._plot_opts)
        plot_opts['invert_axes'] = self.kwds.get('orientation') == 'horizontal'
        opts = dict(plot=plot_opts,
                    style=dict(alpha=self.kwds.get('alpha', 1)))
        return hv.operation.histogram(ds,
                                      dimension=self.data.name).opts(**opts)

    def kde(self):
        plot_opts = dict(self._plot_opts)
        plot_opts['invert_axes'] = self.kwds.get('orientation') == 'horizontal'
        opts = dict(plot=plot_opts,
                    style=dict(alpha=self.kwds.get('alpha', 1)))
        return hv.Distribution(self.data.to_frame(),
                               self.data.name).opts(**opts)


class HoloViewsSeriesPlotMethods(FramePlotMethods, param.Parameterized):
    """Series plotting accessor and method

    Examples
    --------
    >>> s.plot.line()
    >>> s.plot.bar()
    >>> s.plot.hist()

    Plotting methods can also be accessed by calling the accessor as a method
    with the ``kind`` argument:
    ``s.plot(kind='line')`` is equivalent to ``s.plot.line()``
    """

    kind = param.ObjectSelector(default='line',
                                objects=['line', 'bar', 'barh', 'box', 'hist'])

    @property
    def engine_name(self):
        return 'holoviews'

    def __call__(self, kind='line', ax=None,
                 subplots=False, sharex=None, sharey=False, layout=None,
                 figsize=None, use_index=True, title=None, grid=False,
                 legend=True, style=None, logx=False, logy=False, loglog=False,
                 xticks=None, yticks=None, xlim=None, ylim=None,
                 rot=None, fontsize=None, colormap=None, table=False,
                 yerr=None, xerr=None,
                 secondary_y=False, sort_columns=False, **kwds):
        converter = HoloViewsSeriesConverter(
            self._data, ax=ax, figsize=figsize,
            use_index=use_index, title=title, grid=grid,
            legend=legend, style=style, logx=logx, logy=logy,
            loglog=loglog, xticks=xticks, yticks=yticks,
            xlim=xlim, ylim=ylim, rot=rot, fontsize=fontsize,
            colormap=colormap, table=table, yerr=yerr,
            xerr=xerr, secondary_y=secondary_y,
            **kwds)
        return converter(kind)

    def line(self, **kwds):
        """Line plot

        Parameters
        ----------
        **kwds : optional
            Keyword arguments to pass on to :py:meth:`pandas.Series.plot`.

        Returns
        -------
        axes : matplotlib.AxesSubplot or np.array of them
        """
        return self(kind='line', **kwds)

    def bar(self, **kwds):
        """Vertical bar plot

        Parameters
        ----------
        **kwds : optional
            Keyword arguments to pass on to :py:meth:`pandas.Series.plot`.

        Returns
        -------
        axes : matplotlib.AxesSubplot or np.array of them
        """
        return self(kind='bar', **kwds)

    def barh(self, **kwds):
        """Horizontal bar plot

        Parameters
        ----------
        **kwds : optional
            Keyword arguments to pass on to :py:meth:`pandas.Series.plot`.

        Returns
        -------
        axes : matplotlib.AxesSubplot or np.array of them
        """
        return self(kind='barh', **kwds)

    def box(self, **kwds):
        """Boxplot

        Parameters
        ----------
        **kwds : optional
            Keyword arguments to pass on to :py:meth:`pandas.Series.plot`.

        Returns
        -------
        axes : matplotlib.AxesSubplot or np.array of them
        """
        return self(kind='box', **kwds)

    def hist(self, bins=10, **kwds):
        """Histogram

        Parameters
        ----------
        bins: integer, default 10
            Number of histogram bins to be used
        **kwds : optional
            Keyword arguments to pass on to :py:meth:`pandas.Series.plot`.

        Returns
        -------
        axes : matplotlib.AxesSubplot or np.array of them
        """
        return self(kind='hist', bins=bins, **kwds)

    def kde(self, **kwds):
        """Kernel Density Estimate plot

        Parameters
        ----------
        **kwds : optional
            Keyword arguments to pass on to :py:meth:`pandas.Series.plot`.

        Returns
        -------
        axes : matplotlib.AxesSubplot or np.array of them
        """
        return self(kind='kde', **kwds)

    density = kde

    def area(self, **kwds):
        """Area plot

        Parameters
        ----------
        **kwds : optional
            Keyword arguments to pass on to :py:meth:`pandas.Series.plot`.

        Returns
        -------
        axes : matplotlib.AxesSubplot or np.array of them
        """
        return self(kind='area', **kwds)
