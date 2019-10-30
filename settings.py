from dotenv import load_dotenv
import os
load_dotenv()

GITHUB_ACCESS_TOKEN = os.getenv('GITHUB_ACCESS_TOKEN')
REPO = 'openworm/geppetto-client'
USAGE_REPOS = ['VirtualFlyBrain/geppetto-vfb', 'OpenSourceBrain/geppetto-osb', 'openworm/geppetto-application',
               'MetaCell/geppetto-hm', 'MetaCell/geppetto-netpyne', 'MetaCell/geppetto-nwbexplorer']

COMPONENTS_FOLDER_PATH = ['js/components/controls']
# COMPONENTS_FOLDER_PATH = ['js/components/controls', 'js/components/interface', 'js/components/widgets']

COMPONENTS_FOLDER_AUX = ['controls', 'interface', 'widgets']
