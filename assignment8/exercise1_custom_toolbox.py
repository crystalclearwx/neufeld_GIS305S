import arcpy

def intersect(layer_list, intersect_lyr_name):

    # Run a intersect analysis between the two buffer layers (needs to be a list of layers to intersect)
    arcpy.env.overwriteOutput = True
    arcpy.Intersect_analysis(layer_list, intersect_lyr_name)



def buffer_layer(input_gdb, input_layer, dist):
    # Run a buffer analysis on the input_layer with a user specified distance

    # Distance units are always miles
    arcpy.env.overwriteOutput = True
    units = " miles"
    dist = dist + units
    # Output layer will always be named input layer + "_buf
    output_layer = fr"C:\Users\cryst\gis_programming\assignment_1b\worley_modelbuilder.gdb\buf_{input_layer}"
    # Always use buffer parameters FULL, ROUND, ALL
    buf_layer = input_gdb + input_layer
    arcpy.Buffer_analysis(buf_layer, output_layer,
                          dist, "FULL", "ROUND", "ALL")

    return output_layer

def main():
    # Define your workspace and point it at the modelbuilder.gdb
    arcpy.env.workspace = r"C:\Users\cryst\gis_programming\assignment_1b\worley_modelbuilder.gdb"
    arcpy.env.overwriteOutput = True

    # Buffer cities
    input_gdb = r"C:\Users\cryst\gis_programming\Admin\AdminData.gdb\USA\\"

    # Change me this next line below to use GetParamters!!
    dist_cities = arcpy.GetParameterAsText(0)

    buf_cities = buffer_layer(input_gdb, "cities", dist_cities)

    # Change me this next line below to use GetParamters!!
    #print("Buffer layer " + buf_cities + " created.")

    # Buffer rivers
    # Change me this next line below to use GetParamters!!
    dist_rivers = arcpy.GetParameterAsText(1)
    buf_rivers = buffer_layer(input_gdb, "us_rivers", dist_rivers)
    #print("Buffer layer " + buf_rivers + " created.")

    # Define lyr_list variable
    # with names of input layers to intersect
    # Ask the user to define an output layer name
    # Change me this next line below to use GetParamters!!
    intersect_lyr_name = arcpy.GetParameterAsText(2)
    layer_list = [buf_rivers, buf_cities]
    intersect(layer_list, intersect_lyr_name)
    #print(f"New intersect layer generated called: {intersect_lyr_name}")

    # Get the project
    aprx = arcpy.mp.ArcGISProject("CURRENT")
    map_doc = aprx.listMaps()[0]
    map_doc.addDataFromPath(rf"C:\Users\cryst\gis_programming\assignment_1b\worley_modelbuilder.gdb\{intersect_lyr_name}")

    #aprx.save()


if __name__ == '__main__':
    main()