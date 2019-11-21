from dotenv import load_dotenv
import os
load_dotenv()

GITHUB_ACCESS_TOKEN = os.getenv('GITHUB_ACCESS_TOKEN')
REPO = 'openworm/geppetto-client'
USAGE_REPOS = [['VirtualFlyBrain/geppetto-vfb', 'development'], ['OpenSourceBrain/geppetto-osb', 'master'],
                ['openworm/geppetto-application', 'master'], ['MetaCell/geppetto-hm', 'master'],
                ['MetaCell/geppetto-netpyne', 'master'], ['MetaCell/nwbexplorer', 'master'],
                ['openworm/geppetto-client', 'master'], ['MetaCell/geppetto-hnn', 'master']]


COMPONENTS_FOLDER_PATH = ['js/components/controls', 'js/components/interface', 'js/components/widgets']

COMPONENTS_FOLDER_AUX = ['controls', 'interface', 'widgets']

OUTPUT_FILE = "docs/stats.csv"

USAGE_MAP = {
    'FORM': 'interface/form/Form',
    'PANEL': 'controls/panel/Panel',
    'LOGO': 'interface/logo/Logo',
    'LOADINGSPINNER': 'interface/loadingSpinner/LoadingSpinner',
    'SAVECONTROL': 'interface/save/SaveControl',
    'TOGGLEBUTTON': 'controls/toggleButton/ToggleButton',
    'CONTROLPANEL': 'interface/controlPanel/controlpanel',
    'SPOTLIGHT': 'interface/spotlight/spotlight',
    'MENUBUTTON': 'controls/menuButton/MenuButton',
    'FOREGROUND': 'interface/foregroundControls/ForegroundControls',
    'EXPERIMENTSTABLE': 'interface/experimentsTable/ExperimentsTable',
    'HOME': 'interface/home/HomeControl',
    'SIMULATIONCONTROLS': 'interface/simulationControls/ExperimentControls',
    'CAMERACONTROLS': 'interface/cameraControls/CameraControls',
    'SHARE': 'interface/share/Share',
    'INFOMODAL': 'controls/modals/InfoModal',
    'MDMODAL': 'controls/modals/MarkDownModal',
    'QUERY': 'interface/query/query',
    'TUTORIAL': 'interface/tutorial/Tutorial',
    'PYTHONCONSOLE': 'interface/pythonConsole/PythonConsole',
    'DICOMVIEWER': 'interface/dicomViewer/DicomViewer',
    'GOOGLEVIEWER': 'interface/googleViewer/GoogleViewer',
    'BIGIMAGEVIEWER': 'interface/bigImageViewer/BigImageViewer',
    'CAROUSEL': 'interface/carousel/Carousel',
    'CANVAS': 'interface/3dCanvas/Canvas',
    'MOVIEPLAYER': 'interface/moviePlayer/MoviePlayer',
    'TREE': 'interface/tree/Tree',
    'CONSOLE': 'interface/console/Console',
    'LINKBUTTON': 'interface/linkButton/LinkButton',
    'BUTTONBAR': 'interface/buttonBar/ButtonBar',
    'DRAWER': 'interface/drawer/TabbedDrawer',
    'GEPPETTO.Widgets.PLOT': 'plot/controllers/PlotsController',
    'GEPPETTO.Widgets.POPUP': 'popup/controllers/PopupController',
    'GEPPETTO.Widgets.TREEVISUALISERDAT': 'treevisualiser/treevisualiserdat/controllers/TreeVisualiserControllerDAT',
    'GEPPETTO.Widgets.VARIABLEVISUALISER': 'variablevisualiser/controllers/VariableVisualiserController',
    'GEPPETTO.Widgets.CONNECTIVITY': 'connectivity/controllers/ConnectivityController',
    'GEPPETTO.Widgets.STACKVIEWER': 'stackViewer/controllers/StackViewerController',
}