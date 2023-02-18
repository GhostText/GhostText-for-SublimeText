from contextlib import contextmanager

import sublime
from sublime_plugin import EventListener
import json


class OnSelectionModifiedListener(EventListener):
    """
    Handles content changes, each changes gets send with the given web socket server to the client.
    """
    _bind_views = {}
    _disabled = set()

    def on_selection_modified(self, view):
        vid = view.id()
        if (
            vid not in OnSelectionModifiedListener._bind_views
            or vid in self._disabled
        ):
            return

        changed_text = view.substr(sublime.Region(0, view.size()))
        selections = OnSelectionModifiedListener._get_selections(view)
        response = json.dumps({
            'title': view.name(),
            'text':  changed_text,
            'syntax': view.scope_name(0),
            'selections': selections
        })

        OnSelectionModifiedListener._bind_views[view.id()].send_message(response)

    @classmethod
    @contextmanager
    def disabled(cls, view):
        vid = view.id()
        cls._disabled.add(vid)
        try:
            yield
        finally:
            cls._disabled.remove(vid)

    def on_close(self, view):
        if view.id() not in OnSelectionModifiedListener._bind_views:
            return

        print("View with id: {} closed".format(view.id()))
        OnSelectionModifiedListener._bind_views[view.id()].initiate_close()
        OnSelectionModifiedListener.unbind_view(view)

    @staticmethod
    def bind_view(view, web_socket_server):
        """
        Binds a view to a WebSocket.
        """
        print("Bind view with id: {}".format(view.id()))
        OnSelectionModifiedListener._bind_views[view.id()] = web_socket_server

    @classmethod
    def unbind_all_views(cls):
        """
        Close all websocket servers.
        """
        for vid, server in cls._bind_views.items():
            server.initiate_close()
        cls._bind_views.clear()

    @staticmethod
    def unbind_view(view):
        """
        Unbinds a view connected to a WebSocket.
        """
        OnSelectionModifiedListener.unbind_view_by_id(view.id())

    @staticmethod
    def unbind_view_by_id(view_id):
        """
        Unbinds a view specified by it's id connected to a WebSocket.
        """
        print("Unbind view with id: {}".format(view_id))
        if view_id in OnSelectionModifiedListener._bind_views:
            del OnSelectionModifiedListener._bind_views[view_id]

    @staticmethod
    def unbind_view_by_web_socket_server_id(web_socket_server):
        """
        Unbinds a view specified by it's WebSocket server.
        """
        view_id_to_unbind = OnSelectionModifiedListener.find_view_id_by_web_socket_server_id(web_socket_server)

        if view_id_to_unbind is not None:
            OnSelectionModifiedListener.unbind_view_by_id(view_id_to_unbind)

    @staticmethod
    def find_view_id_by_web_socket_server_id(web_socket_server):
        """
        Searches a view by the given WebSocket server or returns None.
        """
        for view_id in OnSelectionModifiedListener._bind_views:
            if OnSelectionModifiedListener._bind_views[view_id].get_id() == web_socket_server.get_id():
                return view_id

        return None

    @staticmethod
    def _get_selections(view):
        """
        Returns the selections from the given view.
        """
        selections = []

        for pos in view.sel():
            selections.append({
                'start': pos.begin(),
                'end': pos.end()
            })

        return selections