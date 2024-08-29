
import vtk

# Global variables to store contour points and lines
contour_points = vtk.vtkPoints()
contour_lines = vtk.vtkCellArray()

def form_contour_lines(contour_points): #function to form contour lines 
    num_points = contour_points.GetNumberOfPoints()
    contour_lines = vtk.vtkCellArray()

    for i in range(num_points - 1):
        line = vtk.vtkLine()
        line.GetPointIds().SetId(0, i)
        line.GetPointIds().SetId(1, i + 1)
        contour_lines.InsertNextCell(line)

    return contour_lines

def extract_isocontour_from_cell(data,cell,cell_values, iso_value,vertex_coordinates,dataArr):
    global contour_points, contour_lines

    contour_segments= [ # segments possible for each 16 cases
        [],
        [[0, 1],[2, 0]],
        [[1, 3],[0, 1]],
        [[0, 2],[1, 3]],
        [[2, 3],[1, 3]],
        [[0, 2],[2, 3],[0, 1],[1, 3]],
        [[2, 3],[0, 1]],
        [[2, 0],[2, 3]],
        [[0, 2],[2, 3]],
        [[2, 3],[0, 1]],
        [[0, 2],[0, 1],[1, 3],[3, 2]],
        [[2, 3],[3, 1]],
        [[0, 2],[1, 3]],
        [[0, 1],[1, 3]],
        [[2, 0],[0, 1]],
        []
    ]
    
    contour_case = 0 #finding which contour case the cell belongs to
    for i in range(4):
        if cell_values[i] >= iso_value:
            contour_case |= 1 << i
            
    contour_curr = contour_segments[contour_case] #get segments corresponding to the segments
    
    interpolated_contour_points=[] # interpolation points list - as we need to traverse the contour vertices in contour clockwise direction starting from first contour vertices,so we append this to list and form lines starting from first contour point
    if(contour_case==5 or contour_case ==10): #ambiguous cases - 2 contour segments
        for intersecting_vertices in contour_curr: # finding vertices which intersect
            vertices=[] # intersecting vertices
            pressure_val=[] # pressure values corresponding to each vertex
            for vertex in intersecting_vertices:
                vid=cell.GetPointId(vertex)#getting vertex id
                curr=data.GetPoint(vid) #getting the vertices
                press=dataArr.GetTuple1(vid)
                vertices.append(curr)
                pressure_val.append(press)
            #finding intersection point in a segment through interpolation
            v1,v2=vertices[0],vertices[1]
            value1,value2=pressure_val[0],pressure_val[1]
            if(value1==value2):#to avoid divide by zero 
                t=0.5
            else:
                t = (iso_value - value1) / (value2 - value1) #interpolation factor
            interpolated_contour_points.append(interpolate_point_vertices(v1, v2, t))
        i=0
        line=vtk.vtkLine()
        line.GetPointIds().SetNumberOfIds(len(interpolated_contour_points))
        for point in interpolated_contour_points:
            point_id=contour_points.InsertNextPoint(point)
            line.GetPointIds().SetId(i,point_id)
            i+=1
            
        contour_lines.InsertNextCell(line)
                
                
                
                
                
    elif(contour_curr==[]):#all pressure values either >< isoval
        empty=vtk.vtkIdList()
        contour_lines.InsertNextCell(empty)
        
    else:# general cell - single segment
        line=vtk.vtkLine()
        i=0
        for intersecting_vertices in contour_curr: # finding vertices which intersect a segment
            vertices=[] # intersecting vertices
            pressure_val=[] # pressure values corresponding to each vertex
            for vertex in intersecting_vertices:
                vid=cell.GetPointId(vertex)#getting vertex id
                curr=data.GetPoint(vid) #getting the vertices
                press=dataArr.GetTuple1(vid)
                vertices.append(curr)
                pressure_val.append(press)
            #finding intersection point in a segment through interpolation
            v1,v2=vertices[0],vertices[1]
            value1,value2=pressure_val[0],pressure_val[1]
            if(value1==value2):#to avoid divide by zero 
                t=0.5
            else:
                t = (iso_value - value1) / (value2 - value1) #interpolation factor
            contour_point_local = interpolate_point_vertices(v1, v2, t)
            id1=contour_points.InsertNextPoint(contour_point_local)
            line.GetPointIds().SetId(i,id1)
            i+=1
        contour_lines.InsertNextCell(line)
        

def interpolate_point_vertices(v1, v2, t):
    x1, y1,z1 = v1
    x2, y2,z2 = v2
    x = x1 + (x2 - x1) * t
    y = y1 + (y2 - y1) * t
    z = z1 + (z2 - z1) * t
    return x, y,z



# Now contour_polydata contains all contour points and lines from all cells




## Import VTK
from vtk import *

## Load data
#######################################
reader = vtkXMLImageDataReader()
reader.SetFileName('/Users/gopichand./Desktop/2ndsem/big_data/Assignment_1/Data/Isabel_2D.vti')
reader.Update()
data = reader.GetOutput()
iso_value=int(input("Enter iso value between -1468 to 630:"))
## Query how many cells the dataset has
#######################################
numCells = data.GetNumberOfCells()
for i in range(numCells):
    ## Get a single cell from the list of cells
    ###########################################
    cell = data.GetCell(i) ## cell index = 0

   
    pid1 = cell.GetPointId(0)
    pid2 = cell.GetPointId(1)
    pid3 = cell.GetPointId(3)
    pid4 = cell.GetPointId(2)

#     ## Print the 1D indices of the corner points
#     ############################################
#     print('1D indices of the cell corner points:')
#     print(pid1,pid2,pid3,pid4) ## in counter-clockwise order


    ## Get values at each vertex
    ## First Get the array
    dataArr = data.GetPointData().GetArray('Pressure')
    val1 = dataArr.GetTuple1(pid1)
    val2 = dataArr.GetTuple1(pid2)
    val3 = dataArr.GetTuple1(pid3)
    val4 = dataArr.GetTuple1(pid4)
    vertex_coordinates=[]
    if(i==0):
        print(val1,val2,val3,val4)
    ## Print the locations (3D coordinates) of the points
    #######################################################
    vertex_coordinates.append(data.GetPoint(pid1))
    vertex_coordinates.append(data.GetPoint(pid2))
    vertex_coordinates.append(data.GetPoint(pid3))
    vertex_coordinates.append(data.GetPoint(pid4))
    
    cellvalues=[val1,val2,val3,val4]
    extract_isocontour_from_cell(data,cell,cellvalues,iso_value,vertex_coordinates,dataArr)
    
    
    
# After iterating through all cells
# Create a polydata with global contour points and lines
contour_polydata = vtk.vtkPolyData()
contour_polydata.SetPoints(contour_points)
contour_polydata.SetLines(contour_lines)

# Write isocontour to VTKPolyData file
writer = vtk.vtkXMLPolyDataWriter()
writer.SetFileName("deepak4.vtp")
writer.SetInputData(contour_polydata)
writer.Write()






