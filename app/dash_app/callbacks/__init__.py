"""
Callback registration for the Healthcare Dashboard.

This module wires together tab-switching logic and registers
callbacks for each feature-specific callback module.
"""

from dash import Output, Input
from ..layouts.operational_layout import operational_layout
from ..layouts.pathway_layout import pathway_layout
from ..layouts.clinician_layout import clinician_layout
from ..layouts.admin_layout import admin_layout
from ..layouts.mdt_layout import mdt_layout
from ..layouts.referral_layout import referral_layout
from .operational_callbacks import register_operational_callbacks
from .pathway_callbacks import register_pathway_callbacks
from .clinician_callbacks import register_clinician_callbacks
from .admin_callbacks import register_admin_callbacks
from .mdt_callbacks import register_mdt_callbacks
from .referral_callbacks import register_referral_callbacks

def register_callbacks(app, data_loader):
    """
    Register all callbacks for the dashboard.

    Args:
        app (dash.Dash): The Dash app instance.
    """
    @app.callback(
        Output('tabs-content', 'children'),
        Input('dropdown-tabs', 'value')
    )
    def render_content(tab):
        """
        Render content based on the selected tab.

        Args:
            tab (str): The selected tab value.

        Returns:
            dash.html.Div: The corresponding layout for the selected tab.
        """
        if tab == 'tab-1':
            return operational_layout()
        if tab == 'tab-2':
            return pathway_layout()
        if tab == 'tab-3':
            return clinician_layout()
        if tab == 'tab-4':
            return admin_layout()
        if tab == 'tab-5':
            return mdt_layout()
        if tab == 'tab-6':
            return referral_layout()
        return None

    register_operational_callbacks(app, data_loader)
    register_pathway_callbacks(app, data_loader)
    register_clinician_callbacks(app, data_loader)
    register_admin_callbacks(app, data_loader)
    register_mdt_callbacks(app, data_loader)
    register_referral_callbacks(app, data_loader)
