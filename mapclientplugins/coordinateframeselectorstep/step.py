'''
MAP Client Plugin Step
'''
import json

from PySide2 import QtGui

from mapclient.mountpoints.workflowstep import WorkflowStepMountPoint
from mapclientplugins.coordinateframeselectorstep.configuredialog import ConfigureDialog
import os.path
import string


class CoordinateFrameSelectorStep(WorkflowStepMountPoint):
    '''
    Skeleton step which is intended to be a helpful starting point
    for new steps.
    '''

    def __init__(self, location):
        super(CoordinateFrameSelectorStep, self).__init__('Coordinate Frame Selector', location)
        self._configured = False  # A step cannot be executed until it has been configured.
        self._category = 'Utility'
        # Add any other initialisation code here:
        self._icon = QtGui.QImage(':/coordinateframeselectorstep/images/utility.png')
        # Ports:
        self.addPort(('http://physiomeproject.org/workflow/1.0/rdf-schema#port',
                      'http://physiomeproject.org/workflow/1.0/rdf-schema#provides',
                      'http://physiomeproject.org/workflow/1.0/rdf-schema#coordinate_description'))
        self.addPort(('http://physiomeproject.org/workflow/1.0/rdf-schema#port',
                      'http://physiomeproject.org/workflow/1.0/rdf-schema#uses',
                      'http://physiomeproject.org/workflow/1.0/rdf-schema#file_location'))
        self.addPort(('http://physiomeproject.org/workflow/1.0/rdf-schema#port',
                      'http://physiomeproject.org/workflow/1.0/rdf-schema#uses',
                      'http://physiomeproject.org/workflow/1.0/rdf-schema#file_location'))
        # Port data:
        self._portData0 = None  # http://physiomeproject.org/workflow/1.0/rdf-schema#coordinate_description
        self._portData1 = None  # http://physiomeproject.org/workflow/1.0/rdf-schema#file_location
        self._portData2 = None  # http://physiomeproject.org/workflow/1.0/rdf-schema#file_location
        # Config:
        self._config = {}
        self._config['identifier'] = ''

    def execute(self):
        '''
        Add your code here that will kick off the execution of the step.
        Make sure you call the _doneExecution() method when finished.  This method
        may be connected up to a button in a widget for example.
        '''
        # Put your execute step code here before calling the '_doneExecution' method.
        csv_file = self._portData1
        data_file = self._portData2

        key, _ = os.path.splitext(os.path.basename(data_file))

        key = key.lower()
        database = {}
        with open(csv_file) as f:
            lines = f.readlines()
            # pop header line
            lines.pop(0)
            for line in lines:
                line = ''.join([c for c in line if c in string.printable])
                line_components = line.strip().split(',')
                if all(line_components) and len(line_components) == 4:
                    origin = self._convertToFloatList(line_components[1])
                    axis = self._convertToFloatList(line_components[2])
                    centroid = self._convertToFloatList(line_components[3])
                    database[line_components[0].lower()] = [origin, axis, centroid]

        if key in database:
            self._portData0 = database[key]
        else:
            self._portData0 = []

        self._doneExecution()

    def _convertToFloatList(self, text):
        split_text = text.split(' ')
        return [float(s) for s in split_text if s]

    def setPortData(self, index, dataIn):
        '''
        Add your code here that will set the appropriate objects for this step.
        The index is the index of the port in the port list.  If there is only one
        uses port for this step then the index can be ignored.
        '''
        if index == 1:
            self._portData1 = dataIn  # http://physiomeproject.org/workflow/1.0/rdf-schema#file_location
        else:
            self._portData2 = dataIn  # http://physiomeproject.org/workflow/1.0/rdf-schema#file_location

    def getPortData(self, index):
        '''
        Add your code here that will return the appropriate objects for this step.
        The index is the index of the port in the port list.  If there is only one
        provides port for this step then the index can be ignored.
        '''
        return self._portData0  # http://physiomeproject.org/workflow/1.0/rdf-schema#coordinate_description

    def configure(self):
        '''
        This function will be called when the configure icon on the step is
        clicked.  It is appropriate to display a configuration dialog at this
        time.  If the conditions for the configuration of this step are complete
        then set:
            self._configured = True
        '''
        dlg = ConfigureDialog(self._main_window)
        dlg.identifierOccursCount = self._identifierOccursCount
        dlg.setConfig(self._config)
        dlg.validate()
        dlg.setModal(True)

        if dlg.exec_():
            self._config = dlg.getConfig()

        self._configured = dlg.validate()
        self._configuredObserver()

    def getIdentifier(self):
        '''
        The identifier is a string that must be unique within a workflow.
        '''
        return self._config['identifier']

    def setIdentifier(self, identifier):
        '''
        The framework will set the identifier for this step when it is loaded.
        '''
        self._config['identifier'] = identifier

    def serialize(self):
        '''
        Add code to serialize this step to string.  This method should
        implement the opposite of 'deserialize'.
        '''
        return json.dumps(self._config, default=lambda o: o.__dict__, sort_keys=True, indent=4)

    def deserialize(self, string):
        '''
        Add code to deserialize this step from string.  This method should
        implement the opposite of 'serialize'.
        '''
        self._config.update(json.loads(string))

        d = ConfigureDialog()
        d.identifierOccursCount = self._identifierOccursCount
        d.setConfig(self._config)
        self._configured = d.validate()
