from .. import core
from ..consts import Index
from .. import FocusPolicy
from .VApplication import VApplication
from .VPalette import VPalette
from .VPainter import VPainter
from .VScreen import VScreenArea
from . import events


class VWidget(core.VObject):
    def __init__(self, parent=None):
        if parent is None:
            parent = VApplication.vApp.rootWidget()

        super().__init__(parent)

        if self.parent() is None:
            self._geometry = (0,0) + VApplication.vApp.screen().size()
        else:
            self._geometry = self.parent().contentsRect()

        self._layout = None
        self._visible_implicit = False
        self._visible_explicit = None
        self._palette = None
        self._enabled = True
        self._active = True
        self._focus_policy = FocusPolicy.NoFocus
        self._needs_update = False

    def keyEvent(self, event):
        pass

    def setFocus(self):
        VApplication.vApp.setFocusWidget(self)

    def hasFocus(self):
        return (self is VApplication.vApp.focusWidget())

    def move(self, pos):
        """
        Sets the size to the specified amount.
        Generates an immediate VMoveEvent if the widget is visible.
        If not visible, the widget will receive it as soon as made visible

        Arguments:
            size: a 2-tuple (x, y)
        """
        if not isinstance(pos, tuple) or len(pos) != 2:
            raise TypeError("Invalid pos argument")

        self.setGeometry(pos+self.size())

    def resize(self, size):
        """
        Sets the size to the specified amount.
        Generates an immediate VResizeEvent if the widget is visible.
        If not visible, the widget will receive it as soon as made visible

        Arguments:
            size: a 2-tuple (width, height)
        """

        if not isinstance(size, tuple) or len(size) != 2:
            raise TypeError("Invalid size argument")

        self.setGeometry(self.pos()+size)

    def size(self):
        """
        Returns:
            the widget current size as a 2-tuple (width, height)
        """
        return (self.geometry()[Index.RECT_WIDTH], self.geometry()[Index.RECT_HEIGHT])

    def rect(self):
        """
        Returns:
            The widget current rect as a 4-tuple (0, 0, width, height).
        """
        return (0,0)+self.size()

    def absoluteRect(self):
        return self.mapToGlobal((0,0))+self.size()

    def geometry(self):
        """
        Returns the geometry of the widget.

        Returns:
            A 4-tuple with (x, y, width, height)
        """
        return self._geometry

    def width(self):
        """
        Returns the width of the widget.

        Returns:
            integer
        """
        return self.geometry()[Index.RECT_WIDTH]

    def height(self):
        """
        Returns the height of the widget.

        Returns:
            integer
        """
        return self.geometry()[Index.RECT_HEIGHT]

    def pos(self):
        """
        Returns the position of the widget within its parent.

        Returns:
            A 2-tuple of integers
        """
        geometry = self.geometry()
        return (geometry[Index.RECT_X], geometry[Index.RECT_Y])

    def x(self):
        """
        Returns the x position of the widget within its parent.

        Returns:
            integer
        """
        geometry = self.geometry()
        return geometry[Index.RECT_X]

    def y(self):
        """
        Returns the y position of the widget within its parent.

        Returns:
            integer
        """
        geometry = self.geometry()
        return geometry[Index.RECT_Y]

    def show(self):
        self.setVisible(True)

    def hide(self):
        self.setVisible(False)

    def setVisible(self, visible):
        self.logger.info("Setting explicit visibility for %s : %s" % (str(self), str(visible)))
        visible_before = self.isVisible()
        self._visible_explicit = visible

        if visible and not visible_before:
            VApplication.vApp.postEvent(self,events.VShowEvent())
        elif not visible and visible_before:
            VApplication.vApp.postEvent(self,events.VHideEvent())

        for w in self.children():
            w.setVisibleImplicit(visible)

    def setVisibleImplicit(self, visible):
        self.logger.info("Setting implicit visibility for %s : %s" % (str(self), str(visible)))
        self._visible_implicit = visible

        if visible:
            VApplication.vApp.postEvent(self,events.VShowEvent())
        else:
            VApplication.vApp.postEvent(self,events.VHideEvent())

        for w in self.children():
            w.setVisibleImplicit(visible)

    def isVisible(self):
        return self._visible_explicit if self._visible_explicit is not None else self._visible_implicit

    def minimumSize(self):
        return (0,0)

    def addLayout(self, layout):
        self._layout = layout
        self._layout.setParent(self)

    def setGeometry(self, rect):

        old_geometry = self._geometry

        min_size = self.minimumSize()
        self._geometry = (rect[Index.RECT_X],
                          rect[Index.RECT_Y],
                          max(min_size[Index.SIZE_WIDTH], rect[Index.RECT_WIDTH]),
                          max(min_size[Index.SIZE_HEIGHT], rect[Index.RECT_HEIGHT])
                         )

        if self.isVisible():
            deliver_routine = VApplication.vApp.sendEvent
        else:
            deliver_routine = VApplication.vApp.postEvent

        if  (old_geometry[Index.RECT_X], old_geometry[Index.RECT_Y])  \
            != (self._geometry[Index.RECT_X], self._geometry[Index.RECT_Y]):

            deliver_routine(self, events.VMoveEvent())

        if (old_geometry[Index.RECT_WIDTH], old_geometry[Index.RECT_WIDTH]) \
            != (self._geometry[Index.RECT_HEIGHT], self._geometry[Index.RECT_HEIGHT]):

            deliver_routine(self, events.VResizeEvent())

    def mapToGlobal(self, pos):
        """
        Given a position pos in coordinates relative to this widget, return the coordinate
        in absolute screen coordinates.

        Arguments:
            pos: 2-tuple (x,y)

        Returns:
            a 2-tuple (x,y) with the absolute coordinates
        """
        top_left = self.pos()
        if self.parent() is None:
            return (pos[Index.X]+top_left[Index.X], pos[Index.Y]+top_left[Index.Y])

        parent_corner = self.parent().mapToGlobal((0,0))
        return ( parent_corner[Index.X] + top_left[Index.X] + pos[Index.X],
                 parent_corner[Index.Y] + top_left[Index.Y] + pos[Index.Y]
                 )

    def screenArea(self):
        abs_pos_topleft = self.mapToGlobal((0,0))

        return VScreenArea( VApplication.vApp.screen(),
                            abs_pos_topleft + self.size()
                          )

    def event(self, event):
        self.logger.info("Event %s. Receiver %s" % (str(event), str(self)))

        if isinstance(event, events.VPaintEvent):
            if not self.isVisible():
                return True
            self.paintEvent(event)
            self._needs_update = False

        elif isinstance(event, events.VFocusEvent):
            if self.isVisible():
                if event.eventType() == core.VEvent.EventType.FocusIn:
                    self.focusInEvent(event)
            else:
                if event.eventType() == core.VEvent.EventType.FocusOut:
                    self.focusOutEvent(event)

            self.update()

        elif isinstance(event, events.VHideEvent):
            self.hideEvent(event)

            for w in self.depthFirstFullTree():
                self.logger.info("Widget %s in tree" % str(w))
                if not w.isVisible():
                    continue
                self.logger.info("Repainting widget %s" % str(w))
                w.update()

        elif isinstance(event, events.VShowEvent):
            self.showEvent(event)

            for w in self.depthFirstFullTree():
                self.logger.info("Widget %s in tree" % str(w))
                if not w.isVisible():
                    continue
                w.update()

        elif isinstance(event, events.VMoveEvent):
            if not self.isVisible():
                return True

            self.moveEvent(event)

            for w in self.depthFirstFullTree():
                self.logger.info("Widget %s in tree" % str(w))
                if not w.isVisible():
                    continue
                w.update()

        elif isinstance(event, events.VResizeEvent):
            if not self.isVisible():
                return True

            self.resizeEvent(event)

            for w in self.depthFirstFullTree():
                self.logger.info("Widget %s in tree" % str(w))
                if not w.isVisible():
                    continue
                w.update()
        else:
            return super().event(event)

        return True

    def paintEvent(self, event):
        painter = VPainter(self)
        #if self._layout is not None:
        #    self._layout.apply()

        size = self.size()

        string = ' '*size[Index.SIZE_WIDTH]
        for i in range(0, size[Index.SIZE_HEIGHT]):
            painter.drawText( (0, i), string)
    def needsUpdate(self):
        return self._needs_update

    def focusInEvent(self, event):
        self.logger.info("FocusIn event")

    def focusOutEvent(self, event):
        self.logger.info("FocusOut event")

    def hideEvent(self, event):
        self.logger.info("Hide event")

    def moveEvent(self, event):
        self.logger.info("Move event")

    def showEvent(self, event):
        self.logger.info("Show event")

    def resizeEvent(self, event):
        self.logger.info("Resize event")

    def setFocusPolicy(self, policy):
        self._focus_policy = policy

    def focusPolicy(self):
        return self._focus_policy

    def isEnabled(self):
        return self._enabled

    def isActive(self):
        return self._active

    def setActive(self, active):
        self._active = active

    def setEnabled(self, enabled):
        self._enabled = enabled

    def palette(self):
        if self._palette is None:
            self._palette = VApplication.vApp.palette().copy()

        return self._palette

    def setColors(self, fg=None, bg=None):
        self.palette().setColor(VPalette.ColorGroup.Active, VPalette.ColorRole.WindowText, fg)
        self.palette().setColor(VPalette.ColorGroup.Active, VPalette.ColorRole.Window, bg)

    def colors(self, color_group = VPalette.ColorGroup.Active):
        fg = self.palette().color(color_group, VPalette.ColorRole.WindowText)
        bg = self.palette().color(color_group, VPalette.ColorRole.Window)

        return (fg, bg)

    def currentColors(self):
        if self.isActive():
            color_group = VPalette.ColorGroup.Active
        else:
            if isEnabled(self):
                color_group = VPalette.ColorGroup.Inactive
            else:
                color_group = VPalette.ColorGroup.Disabled
        return self.colors(color_group)

    def update(self):
        self._needs_update = True

    def contentsRect(self):
        # XXX Check because I think we also have to subtract border and padding
        margins = self.contentsMargins()
        return (margins[Index.MARGIN_LEFT],
                margins[Index.MARGIN_TOP],
                self.width()-margins[Index.MARGIN_LEFT]-margins[Index.MARGIN_RIGHT],
                self.height()-margins[Index.MARGIN_TOP]-margins[Index.MARGIN_BOTTOM]
                )

    def contentsMargins(self):
        # XXX not sure about the definition of margins for qt
        return (0,0,0,0)


#    def accessibleName(self):


# QByteArray  saveGeometry () const
    def fontInfo(self):
        pass

#    def layout ()
#    def actions ()
#    def locale ()
#    def QMargins contentsMargins ():
#    def QPalette::ColorRole backgroundRole () const
#    def QPalette::ColorRole foregroundRole () const
#    def QPoint  mapFrom ( QWidget * parent, const QPoint & pos ) const
#    def QPoint  mapFromGlobal ( const QPoint & pos ) const
#    def QPoint  mapFromParent ( const QPoint & pos ) const
#    def QPoint  mapTo ( QWidget * parent, const QPoint & pos ) const
#    def QPoint  mapToGlobal ( const QPoint & pos ) const
#    def QPoint  mapToParent ( const QPoint & pos ) const
#    QRect   childrenRect () const
#    QRect   contentsRect () const
#    QRect   frameGeometry () const
#    QRect   normalGeometry () const
#    QRegion childrenRegion () const
#    QRegion mask () const
#    QRegion visibleRegion () const
#    QSize   baseSize () const
#    QSize   frameSize () const
#    QSize   maximumSize () const
#    QSize   minimumSize () const
#    QSizePolicy sizePolicy () const
#    QString windowRole () const
#    QString windowTitle () const
#    QWidget *   childAt ( const QPoint & p ) const
#    QWidget *   childAt ( int x, int y ) const
#    QWidget *   focusProxy () const
#    QWidget *   focusWidget () const
#    QWidget *   nativeParentWidget () const
#    QWidget *   nextInFocusChain () const
#    QWidget *   parentWidget () const
#    QWidget *   previousInFocusChain () const
#    QWidget *   window () const
#    QWindowSurface *    windowSurface () const (preliminary)
#    Qt::ContextMenuPolicy   contextMenuPolicy () const
#    Qt::FocusPolicy focusPolicy () const
#    Qt::InputMethodHints    inputMethodHints () const
#    Qt::LayoutDirection layoutDirection () const
#    Qt::WindowFlags windowFlags () const
#    Qt::WindowModality  windowModality () const
#    Qt::WindowStates    windowState () const
#    Qt::WindowType  windowType () const
#    bool    autoFillBackground () const
#    bool    close ()
#    bool    hasEditFocus () const
#    bool    hasFocus () const
#    bool    isActiveWindow () const
#    bool    isAncestorOf ( const QWidget * child ) const
#    bool    isEnabled () const
#    bool    isEnabledTo ( QWidget * ancestor ) const
#    bool    isFullScreen () const
#    bool    isHidden () const
#    bool    isMaximized () const
#    bool    isMinimized () const
#    bool    isModal () const
#    bool    isVisible () const
#    bool    isVisibleTo ( QWidget * ancestor ) const
#    bool    isWindow () const
#    bool    isWindowModified () const
#    bool    restoreGeometry ( const QByteArray & geometry )
#    bool    testAttribute ( Qt::WidgetAttribute attribute ) const
#    bool    updatesEnabled () const
#    const QFont &   font () const
#    const QPalette &    palette () const
#    int maximumHeight () const
#    int maximumWidth () const
#    int minimumHeight () const
#    int minimumWidth () const
#    qreal   windowOpacity () const
#    virtual QSize   minimumSizeHint () const
#    virtual QSize   sizeHint () const
#    virtual QVariant    inputMethodQuery ( Qt::InputMethodQuery query ) const
#    virtual int heightForWidth ( int w ) const
#    virtual void    setVisible ( bool visible )
#    void    activateWindow ()
#    void    addAction ( QAction * action )
#    void    addActions ( QList<QAction *> actions )
#    void    adjustSize ()
#    void    clearFocus ()
#    void    clearMask ()
#    void    ensurePolished () const
#    void    getContentsMargins ( int * left, int * top, int * right, int * bottom ) const
#    void    hide ()
#    void    insertAction ( QAction * before, QAction * action )
#    void    insertActions ( QAction * before, QList<QAction *> actions )
#    void    lower ()
#    void    overrideWindowFlags ( Qt::WindowFlags flags )
#    void    raise ()
#    void    removeAction ( QAction * action )
#    void    render ( QPaintDevice * target, const QPoint & targetOffset = QPoint(), const QRegion & sourceRegion = QRegion(), RenderFlags renderFlags = RenderFlags( DrawWindowBackground | DrawChildren ) )
#    void    render ( QPainter * painter, const QPoint & targetOffset = QPoint(), const QRegion & sourceRegion = QRegion(), RenderFlags renderFlags = RenderFlags( DrawWindowBackground | DrawChildren ) )
#    void    repaint ( const QRect & rect )
#    void    repaint ( const QRegion & rgn )
#    void    repaint ( int x, int y, int w, int h )
#    void    repaint ()
#    void    scroll ( int dx, int dy )
#    void    scroll ( int dx, int dy, const QRect & r )
#    void    setAcceptDrops ( bool on )
#    void    setAccessibleDescription ( const QString & description )
#    void    setAccessibleName ( const QString & name )
#    void    setAttribute ( Qt::WidgetAttribute attribute, bool on = true )
#    void    setAutoFillBackground ( bool enabled )
#    void    setBackgroundRole ( QPalette::ColorRole role )
#    void    setBaseSize ( const QSize & )
#    void    setBaseSize ( int basew, int baseh )
#    void    setContentsMargins ( const QMargins & margins )
#    void    setContentsMargins ( int left, int top, int right, int bottom )
#    void    setContextMenuPolicy ( Qt::ContextMenuPolicy policy )
#    void    setDisabled ( bool disable )
#    void    setEditFocus ( bool enable )
#    void    setEnabled ( bool )
#    void    setFixedHeight ( int h )
#    void    setFixedSize ( const QSize & s )
#    void    setFixedSize ( int w, int h )
#    void    setFixedWidth ( int w )
#    void    setFocus ( Qt::FocusReason reason )
#    void    setFocus ()
#    void    setFocusPolicy ( Qt::FocusPolicy policy )
#    void    setFocusProxy ( QWidget * w )
#    void    setFont ( const QFont & )
#    void    setForegroundRole ( QPalette::ColorRole role )
#    void    setGeometry ( const QRect & )
#    void    setGeometry ( int x, int y, int w, int h )
#    void    setHidden ( bool hidden )
#    void    setInputContext ( QInputContext * context )
#    void    setInputMethodHints ( Qt::InputMethodHints hints )
#    void    setLayout ( QLayout * layout )
#    void    setLayoutDirection ( Qt::LayoutDirection direction )
#    void    setLocale ( const QLocale & locale )
#    void    setMask ( const QBitmap & bitmap )
#    void    setMask ( const QRegion & region )
#    void    setMaximumHeight ( int maxh )
#    void    setMaximumSize ( const QSize & )
#    void    setMaximumSize ( int maxw, int maxh )
#    void    setMaximumWidth ( int maxw )
#    void    setMinimumHeight ( int minh )
#    void    setMinimumSize ( const QSize & )
#    void    setMinimumSize ( int minw, int minh )
#    void    setMinimumWidth ( int minw )
#    void    setPalette ( const QPalette & )
#    void    setParent ( QWidget * parent )
#    void    setParent ( QWidget * parent, Qt::WindowFlags f )
#    void    setShortcutAutoRepeat ( int id, bool enable = true )
#    void    setShortcutEnabled ( int id, bool enable = true )
#    void    setSizePolicy ( QSizePolicy )
#    void    setSizePolicy ( QSizePolicy::Policy horizontal, QSizePolicy::Policy vertical )
#    void    setUpdatesEnabled ( bool enable )
#    void    setWindowFilePath ( const QString & filePath )
#    void    setWindowFlags ( Qt::WindowFlags type )
#    void    setWindowModality ( Qt::WindowModality windowModality )
#    void    setWindowModified ( bool )
#    void    setWindowOpacity ( qreal level )
#    void    setWindowRole ( const QString & role )
#    void    setWindowState ( Qt::WindowStates windowState )
#    void    setWindowSurface ( QWindowSurface * surface ) (preliminary)
#    void    setWindowTitle ( const QString & )
#    void    show ()
#    void    showFullScreen ()
#    void    showMaximized ()
#    void    showMinimized ()
#    void    showNormal ()
#    void    stackUnder ( QWidget * w )
#    void    unsetCursor ()
#    void    unsetLayoutDirection ()
#    void    unsetLocale ()
#    void    update ( const QRect & rect )
#    void    update ( const QRegion & rgn )
#    void    update ( int x, int y, int w, int h )
#    void    update ()
#    void    updateGeometry ()
