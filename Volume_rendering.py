#install vtk and import the vtk
import vtk

# Load 3D data by using the vtkXMLImageDataReader
reader = vtk.vtkXMLImageDataReader()
reader.SetFileName("/Users/gopichand./Desktop/2ndsem/big_data/Assignment_1/Data/Isabel_3D.vti")
reader.Update()

# Create color and opacity transfer functions
color_transfer_function = vtk.vtkColorTransferFunction()
color_transfer_function.AddRGBPoint(-4931.54, 0.0, 1.0, 1.0)
color_transfer_function.AddRGBPoint(-2508.95, 0.0, 0.0, 1.0)
color_transfer_function.AddRGBPoint(-1873.9, 0.0, 0.0, 0.5)
color_transfer_function.AddRGBPoint(-1027.16, 1.0, 0.0, 0.0)
color_transfer_function.AddRGBPoint(-298.031, 1.0, 0.4, 0.0)
color_transfer_function.AddRGBPoint(2594.97, 1.0, 1.0, 0.0)

opacity_transfer_function = vtk.vtkPiecewiseFunction()
opacity_transfer_function.AddPoint(-4931.54, 1.0)
opacity_transfer_function.AddPoint(101.815, 0.002)
opacity_transfer_function.AddPoint(2594.97, 0.0)

# Ask user if they want to use Phong shading
use_phong_shading = input("Do you want to use Phong shading? (yes/no): ").lower() == 'yes'

# Create volume mapper
volume_data=reader.GetOutput()
volume_mapper = vtk.vtkSmartVolumeMapper()
volume_mapper.SetInputData(volume_data)
volume_mapper.SetBlendModeToComposite()  # Use compositing for rendering

volume_property = vtk.vtkVolumeProperty()
volume_property.SetColor(color_transfer_function)
volume_property.SetScalarOpacity(opacity_transfer_function)

if use_phong_shading:
    volume_property.ShadeOn()
    volume_property.SetAmbient(0.5)
    volume_property.SetDiffuse(0.5)
    volume_property.SetSpecular(0.5)

volume = vtk.vtkVolume()
volume.SetMapper(volume_mapper)
volume.SetProperty(volume_property)
volume_mapper=volume

# Create outline
outline_filter = vtk.vtkOutlineFilter()
outline_filter.SetInputData(volume_data)

outline_mapper = vtk.vtkPolyDataMapper()
outline_mapper.SetInputConnection(outline_filter.GetOutputPort())

outline_actor = vtk.vtkActor()
outline_actor.SetMapper(outline_mapper)
outline_actor.GetProperty().SetColor(0, 0, 0)  

# Create renderer
renderer = vtk.vtkRenderer()
renderer.SetBackground(1.0, 1.0, 1.0)  # Set background color to white
renderer.AddVolume(volume_mapper)
renderer.AddActor(outline_actor)

# Create render window
render_window = vtk.vtkRenderWindow()
render_window.SetSize(1000, 1000)
render_window.AddRenderer(renderer)

# Create render window interactor
interactor = vtk.vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

# Start the interaction
render_window.Render()
interactor.Start()
