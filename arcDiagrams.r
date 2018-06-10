library(devtools)
install_github('arcdiagram', username='gastonstat')
library(arcdiagram)

setwd("D:\\Documents\\Dropbox\\MSc Data Science\\7CCSMSDW Data Visualisation\\Assignment 2")

carfile = "D:\\Documents\\Dropbox\\MSc Data Science\\7CCSMSDW Data Visualisation\\Assignment 2\\car3.txt"
car3_graph <- read.graph(carfile, format='gml')
edgelist = get.edgelist(car3_graph)

arcplot(edgelist)

vlabels = get.vertex.attribute(car3_graph, 'label') # get label
vgroups = get.vertex.attribute(car3_graph, 'group') # get group
vfill = get.vertex.attribute(car3_graph, 'fill')
values = get.edge.attribute(car3_graph, 'count')

# vertex degree 
degrees = degree(car3_graph)

arcplot(edgelist, cex.labels = 0.7, show.nodes= TRUE, sorted = TRUE,
        col.nodes = '#FFFFFF', bg.nodes=vfill, cex.nodes = log(degrees) + 0.5, pch.nodes=21,
        lwd.nodes = 2, line = -0.5, col.arcs = hsv(0, 0, 0.2, 0.25), lwd.arcs = 1.5 * (values/100))

library(reshape)
library(dplyr)
x = data.frame(vgroups, degrees, vlabels, ind = 1:vcount(car3_graph))
head(x)
y = arrange(x, desc(vgroups), desc(degrees))
new_ord = y$ind

arcplot(edgelist, ordering = new_ord, cex.labels = 0.7, show.nodes= TRUE, sorted = TRUE,
        col.nodes = '#FFFFFF', cex.nodes = 3.5, bg.nodes=vfill, pch.nodes=21,
        lwd.nodes = 2, line = -0.5, col.arcs = hsv(0, 0, 0.2, 0.25), lwd.arcs = 1.5 * (values/100))


# just change this code across all cars
carfile = "D:\\Documents\\Dropbox\\MSc Data Science\\7CCSMSDW Data Visualisation\\Assignment 2\\car2P.txt"
car3_graph <- read.graph(carfile, format='gml')
edgelist = get.edgelist(car3_graph)
vlabels = get.vertex.attribute(car3_graph, 'label') # get label
vgroups = get.vertex.attribute(car3_graph, 'group') # get group
vfill = get.vertex.attribute(car3_graph, 'fill')
values = get.edge.attribute(car3_graph, 'count')
degrees = degree(car3_graph)
x = data.frame(vgroups, degrees, vlabels, ind = 1:vcount(car3_graph))
y = arrange(x, desc(vgroups), desc(degrees))
new_ord = y$ind

arcplot(edgelist, ordering = new_ord, cex.labels = 0.7, show.nodes= TRUE, sorted = TRUE,
        col.nodes = '#FFFFFF', cex.nodes = 3.5, bg.nodes=vfill, pch.nodes=21,
        lwd.nodes = 2, line = -0.5, col.arcs = hsv(0, 0, 0.2, 0.25), lwd.arcs = 1.5 * (values/50))
