from PyQt4 import QtCore, QtGui
from PySchedUI import TemplateParser

class AddJobDialog(QtGui.QDialog):
    def __init__(self, parent=None, templatePath=None):
        QtGui.QDialog.__init__(self, parent)


        self.resize(720, 580)
        self.setWindowTitle("Add Job")
        self.buttonBox = QtGui.QDialogButtonBox(self)
        self.buttonBox.setGeometry(QtCore.QRect(10, 540, 700, 30))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)

        self.frame = QtGui.QFrame(self)
        self.frame.setGeometry(QtCore.QRect(10, 10, 700, 160))
        self.frame.setFrameShape(QtGui.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtGui.QFrame.Raised)

        self.formLayoutWidget = QtGui.QWidget(self.frame)
        self.formLayoutWidget.setGeometry(QtCore.QRect(10, 10, 680, 140))

        self.formLayout = QtGui.QFormLayout(self.formLayoutWidget)
        self.formLayout.setMargin(0)

        self.label = QtGui.QLabel(self.formLayoutWidget)
        self.label.setText("Job Name")

        self.formLayout.setWidget(0, QtGui.QFormLayout.LabelRole, self.label)
        self.jobNameWidget = QtGui.QLineEdit(self.formLayoutWidget)

        self.formLayout.setWidget(0, QtGui.QFormLayout.FieldRole, self.jobNameWidget)
        self.label_2 = QtGui.QLabel(self.formLayoutWidget)
        self.label_2.setText("Job Description:")

        self.formLayout.setWidget(1, QtGui.QFormLayout.LabelRole, self.label_2)
        self.jobDescriptionWidget = QtGui.QPlainTextEdit(self.formLayoutWidget)

        self.formLayout.setWidget(1, QtGui.QFormLayout.FieldRole, self.jobDescriptionWidget)
        self.frame_2 = QtGui.QFrame(self)
        self.frame_2.setGeometry(QtCore.QRect(10, 180, 700, 350))
        self.frame_2.setFrameShape(QtGui.QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QtGui.QFrame.Raised)

        self.formLayoutWidget_2 = QtGui.QWidget(self.frame_2)
        self.formLayoutWidget_2.setGeometry(QtCore.QRect(10, 50, 335, 290))

        self.formLayout_2 = QtGui.QFormLayout(self.formLayoutWidget_2)
        self.formLayout_2.setRowWrapPolicy(QtGui.QFormLayout.WrapAllRows)
        self.formLayout_2.setMargin(0)

        self.label_3 = QtGui.QLabel(self.formLayoutWidget_2)
        self.label_3.setText("Multiple CPUs")
        self.label_3.setWhatsThis(MULTI_CPU_HELP)

        self.formLayout_2.setWidget(0, QtGui.QFormLayout.LabelRole, self.label_3)
        self.multiCpuWidget = QtGui.QCheckBox(self.formLayoutWidget_2)
        self.multiCpuWidget.setWhatsThis(MULTI_CPU_HELP)

        self.formLayout_2.setWidget(0, QtGui.QFormLayout.FieldRole, self.multiCpuWidget)
        self.label_4 = QtGui.QLabel(self.formLayoutWidget_2)
        self.label_4.setText("Required OS:")
        self.label_4.setWhatsThis(REQ_OS_HELP)

        self.formLayout_2.setWidget(1, QtGui.QFormLayout.LabelRole, self.label_4)
        self.reqOSWidget = QtGui.QComboBox(self.formLayoutWidget_2)
        self.reqOSWidget.setWhatsThis(REQ_OS_HELP)

        self.reqOSWidget.addItem("Linux")
        self.formLayout_2.setWidget(1, QtGui.QFormLayout.FieldRole, self.reqOSWidget)
        self.label_5 = QtGui.QLabel(self.formLayoutWidget_2)
        self.label_5.setText("Min CPU Count:")
        self.label_5.setWhatsThis(REQ_CPU_HELP)

        self.formLayout_2.setWidget(2, QtGui.QFormLayout.LabelRole, self.label_5)
        self.minCpuCountWidget = QtGui.QSpinBox(self.formLayoutWidget_2)
        self.minCpuCountWidget.setMinimum(1)
        self.minCpuCountWidget.setWhatsThis(REQ_CPU_HELP)

        self.formLayout_2.setWidget(2, QtGui.QFormLayout.FieldRole, self.minCpuCountWidget)
        self.label_6 = QtGui.QLabel(self.formLayoutWidget_2)    
        self.label_6.setText("Min Memory:")
        self.label_6.setWhatsThis(REQ_MEM_HELP)


        self.formLayout_2.setWidget(3, QtGui.QFormLayout.LabelRole, self.label_6)
        self.minMemoryWidget = QtGui.QSpinBox(self.formLayoutWidget_2)
        self.minMemoryWidget.setMinimum(0)
        self.minMemoryWidget.setWhatsThis(REQ_MEM_HELP)

        self.formLayout_2.setWidget(3, QtGui.QFormLayout.FieldRole, self.minMemoryWidget)
        self.label_7 = QtGui.QLabel(self.formLayoutWidget_2)        
        self.label_7.setText("Files:")
        self.label_7.setWhatsThis(PATH_HELP)

        self.formLayout_2.setWidget(4, QtGui.QFormLayout.LabelRole, self.label_7)
        self.pathWidget = QtGui.QPlainTextEdit(self.formLayoutWidget_2)
        self.pathWidget.setWhatsThis(PATH_HELP)

        self.formLayout_2.setWidget(4, QtGui.QFormLayout.FieldRole, self.pathWidget)
        self.formLayoutWidget_3 = QtGui.QWidget(self.frame_2)
        self.formLayoutWidget_3.setGeometry(QtCore.QRect(355, 50, 335, 290))

        self.formLayout_3 = QtGui.QFormLayout(self.formLayoutWidget_3)
        self.formLayout_3.setRowWrapPolicy(QtGui.QFormLayout.WrapAllRows)
        self.formLayout_3.setMargin(0)

        self.label_8 = QtGui.QLabel(self.formLayoutWidget_3)
        self.label_8.setText("Required Programs:")
        self.label_8.setWhatsThis(PROGRAMS_HELP)

        self.formLayout_3.setWidget(0, QtGui.QFormLayout.LabelRole, self.label_8)
        self.reqProgramsWidget = QtGui.QPlainTextEdit(self.formLayoutWidget_3)
        self.reqProgramsWidget.setWhatsThis(PROGRAMS_HELP)

        self.formLayout_3.setWidget(0, QtGui.QFormLayout.FieldRole, self.reqProgramsWidget)
        self.label_9 = QtGui.QLabel(self.formLayoutWidget_3)
        self.label_9.setText("Compiler:")
        self.label_9.setWhatsThis(COMPILER_HELP)

        self.formLayout_3.setWidget(1, QtGui.QFormLayout.LabelRole, self.label_9)
        self.compilerWidget = QtGui.QLineEdit(self.formLayoutWidget_3)
        self.compilerWidget.setWhatsThis(COMPILER_HELP)

        self.formLayout_3.setWidget(1, QtGui.QFormLayout.FieldRole, self.compilerWidget)
        self.label_10 = QtGui.QLabel(self.formLayoutWidget_3)
        self.label_10.setText("Execution:")
        self.label_10.setWhatsThis(EXECUTION_HELP)

        self.formLayout_3.setWidget(2, QtGui.QFormLayout.LabelRole, self.label_10)
        self.executeWidget = QtGui.QLineEdit(self.formLayoutWidget_3)
        self.executeWidget.setWhatsThis(EXECUTION_HELP)

        self.formLayout_3.setWidget(2, QtGui.QFormLayout.FieldRole, self.executeWidget)
        self.loadButton = QtGui.QPushButton(self.frame_2)
        self.loadButton.setGeometry(QtCore.QRect(10, 10, 130, 30))
        self.loadButton.setText("Load from file...")
        self.loadButton.connect(self.loadButton, QtCore.SIGNAL("clicked()"), self.openTemplate)

        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("accepted()"), self.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("rejected()"), self.reject)
        QtCore.QMetaObject.connectSlotsByName(self)

        if templatePath:
            self.openTemplate(templatePath)

    def createConfigFile(self):
        paths = str(self.pathWidget.document().toPlainText()).split("\n")
        programs = str(self.reqProgramsWidget.document().toPlainText()).split("\n")

        param = {
            "jobName"       : str(self.jobNameWidget.text()),
            "jobDescription": str(self.jobDescriptionWidget.document().toPlainText()),
            "multiCpu"      : self.multiCpuWidget.isChecked(),
            "reqOS"         : str(self.reqOSWidget.currentText()),
            "minCpu"        : self.minCpuCountWidget.value(),
            "minMemory"     : self.minMemoryWidget.value(),
            "paths"         : paths,
            "compilerStr"   : str(self.compilerWidget.text()),
            "reqPrograms"   : programs,
            "executeStr"    : str(self.executeWidget.text())
        }
        return param

    def openTemplate(self, templatePath=None):
        if not templatePath:
            templatePath = QtGui.QFileDialog.getOpenFileName(self, "Select a Template file")
       
        if templatePath:
            info = TemplateParser.ParseTemplate(str(templatePath))
            if info.get("jobName", ""):
                self.jobNameWidget.setText(info.get("jobName", ""))

            if info.get("jobDescription", ""):
                self.jobDescriptionWidget.document().setPlainText(info.get("jobDescription", ""))

            if info.get("multiCpu", False):                
                self.multiCpuWidget.setChecked(info.get("multiCpu", False))

            if info.get("minCpu", 1):
                self.minCpuCountWidget.setValue(info.get("minCpu", 1))

            if info.get("minMemory", 0):
                self.minMemoryWidget.setValue(info.get("minMemory", 0))

            paths = ""
            for p in info.get("paths", []):
                paths += p + "\n"            
            self.pathWidget.appendPlainText(paths.strip())

            progs = ""
            for p in info.get("reqPrograms", []):
                progs += p + "\n"    
            self.reqProgramsWidget.appendPlainText(progs.strip())


            if info.get("compilerStr", ""):
                self.compilerWidget.setText(info.get("compilerStr", ""))

            if info.get("executeStr", ""):
                self.executeWidget.setText(info.get("executeStr", ""))


MULTI_CPU_HELP = """
Check, if the program supports multiple cpu's.
"""

REQ_OS_HELP = """
Changes to this variable may result in not scheduling your job if the given OS 
is not available within the network. For further informations please contact 
your administrator."""

REQ_CPU_HELP =  """
Sets the CPU count that should be at least reserved for the program. Setting 
this to a high value may result in a longer scheduling time till a workstation 
that matches the requirement is free. This option is only used by the parser
if MULTI_CPU is true."""

REQ_MEM_HELP = """
Set this option, if the program needs at least a specific amount of memory to run.
The value given here is stated in MB.
"""

PATH_HELP = """
This section defines the files that are needed by the program. All files 
specified here are send to the server. If a folder is specified the content 
will be send to the server.

Examples:
/home/user/HelloWorld.c will send the file HelloWorld.c to the server
/home/user/foo/ will send the complete folder to the server
/home/user/foo/* will send the content of the folder foo to the server"""

COMPILER_HELP = """
This section is only needed if the program needs to be compiled first. The 
compilation will be done on the server. Please make sure that the needed 
compiler and all libraries are installed on the server or provided via the PATH 
section. If you are using a linux OS it may be simpler to compile the code on 
your machine and link (static linking) all necessary files with the executable.

Example: If you have specified the file HelloWorld.c at the
PATH section and want to compile this file with the
gcc-compiler (installed on the server) the compiler code
should look like:
gcc -o helloWorld HelloWorld.c"""

PROGRAMS_HELP = """
This section is only needed if the program (or - more likely- the script) needs 
a special environment (in this case a special program) to run. Here you can 
provide a list of programs which must be available on the workstation. To use
this feature it is highly recommended to speak with your administrator first 
because the specified program may not be listed within the scheduler and thus 
your program will never be started. In fact it is possible to provide any program
(make sure you provide the name of the executable) and the scheduler will ask 
the workstations for this program but this is not recommended."""

EXECUTION_HELP = """
This section describes how the program should be started on the workstation. 
Here you must provide a bash command like if you would start the program on 
your own machine.

Example:
To start the compiled HelloWorld program simply enter:
helloWorld"""
