import param


class HoloViewsFramePlotMethods(HoloViewsSeriesPlotMethods):
    by = param.String(default=None)

    def __call__(self, x=None, y=None, kind='line', ax=None,
                 subplots=False, sharex=None, sharey=False, layout=None,
                 figsize=None, use_index=True, title=None, grid=False,
                 legend=True, style=None, logx=False, logy=False, loglog=False,
                 xticks=None, yticks=None, xlim=None, ylim=None,
                 rot=None, fontsize=None, colormap=None, table=False,
                 yerr=None, xerr=None,
                 secondary_y=False, sort_columns=False, **kwds):
        converter = HoloViewsFrameConverter(self._data, ax=ax, figsize=figsize,
                           use_index=use_index, title=title, grid=grid,
                           legend=legend, style=style, logx=logx, logy=logy,
                           loglog=loglog, xticks=xticks, yticks=yticks,
                           xlim=xlim, ylim=ylim, rot=rot, fontsize=fontsize,
                           colormap=colormap, table=table, yerr=yerr,
                           xerr=xerr, secondary_y=secondary_y,
                           **kwds)
        return converter(kind, x, y)

    def line(self, x=None, y=None, **kwds):
        """Line plot

        Parameters
        ----------
        x, y : label or position, optional
            Coordinates for each point.
        **kwds : optional
            Keyword arguments to pass on to :py:meth:`pandas.DataFrame.plot`.

        Returns
        -------
        axes : matplotlib.AxesSubplot or np.array of them
        """
        return self(kind='line', x=x, y=y, **kwds)

    def bar(self, x=None, y=None, **kwds):
        """Vertical bar plot

        Parameters
        ----------
        x, y : label or position, optional
            Coordinates for each point.
        **kwds : optional
            Keyword arguments to pass on to :py:meth:`pandas.DataFrame.plot`.

        Returns
        -------
        axes : matplotlib.AxesSubplot or np.array of them
        """
        return self(kind='bar', x=x, y=y, **kwds)

    def barh(self, x=None, y=None, **kwds):
        """Horizontal bar plot

        Parameters
        ----------
        x, y : label or position, optional
            Coordinates for each point.
        **kwds : optional
            Keyword arguments to pass on to :py:meth:`pandas.DataFrame.plot`.

        Returns
        -------
        axes : matplotlib.AxesSubplot or np.array of them
        """
        return self(kind='barh', x=x, y=y, **kwds)

    def box(self, by=None, **kwds):
        """Boxplot

        Parameters
        ----------
        by : string or sequence
            Column in the DataFrame to group by.
        **kwds : optional
            Keyword arguments to pass on to :py:meth:`pandas.DataFrame.plot`.

        Returns
        -------
        axes : matplotlib.AxesSubplot or np.array of them
        """
        return self(kind='box', by=by, **kwds)

    def hist(self, by=None, bins=10, **kwds):
        """Histogram

        Parameters
        ----------
        by : string or sequence
            Column in the DataFrame to group by.
        bins: integer, default 10
            Number of histogram bins to be used
        **kwds : optional
            Keyword arguments to pass on to :py:meth:`pandas.DataFrame.plot`.

        Returns
        -------
        axes : matplotlib.AxesSubplot or np.array of them
        """
        return self(kind='hist', by=by, bins=bins, **kwds)

    def kde(self, **kwds):
        """Kernel Density Estimate plot

        Parameters
        ----------
        **kwds : optional
            Keyword arguments to pass on to :py:meth:`pandas.DataFrame.plot`.

        Returns
        -------
        axes : matplotlib.AxesSubplot or np.array of them
        """
        return self(kind='kde', **kwds)

    density = kde

    def area(self, x=None, y=None, stacked=True, **kwds):
        """Area plot

        Parameters
        ----------
        x, y : label or position, optional
            Coordinates for each point.
        **kwds : optional
            Keyword arguments to pass on to :py:meth:`pandas.DataFrame.plot`.

        Returns
        -------
        axes : matplotlib.AxesSubplot or np.array of them
        """
        return self(kind='area', x=x, y=y, stacked=stacked, **kwds)

    def scatter(self, x, y, s=None, c=None, **kwds):
        """Scatter plot

        Parameters
        ----------
        x, y : label or position, optional
            Coordinates for each point.
        s : scalar or array_like, optional
            Size of each point.
        c : label or position, optional
            Color of each point.
        **kwds : optional
            Keyword arguments to pass on to :py:meth:`pandas.DataFrame.plot`.

        Returns
        -------
        axes : matplotlib.AxesSubplot or np.array of them
        """
        return self(kind='scatter', x=x, y=y, c=c, s=s, **kwds)
