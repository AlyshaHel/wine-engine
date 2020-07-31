//MATCH (n) DETACH DELETE n

// Create wines
LOAD CSV WITH HEADERS FROM 'https://raw.githubusercontent.com/AlyshaHel/wine-engine/master/wine/data/winename_table.csv' AS row
MERGE (wine:Wine {wineID: row.WineID})
  ON CREATE SET wine.wineDesc = row.WineDesc, wine.vintage = toInteger(row.Vintage);

// Create descriptors
LOAD CSV WITH HEADERS FROM 'https://raw.githubusercontent.com/AlyshaHel/wine-engine/master/wine/data/descriptor_table.csv' AS row
MERGE (descriptor:Descriptor {descriptorID: row.DescriptorID})
  ON CREATE SET descriptor.descriptorDesc = row.DescriptorDesc;

// Create colors
LOAD CSV WITH HEADERS FROM 'https://raw.githubusercontent.com/AlyshaHel/wine-engine/master/wine/data/color_table.csv' AS row
MERGE (color:Color {colorID: row.ColorID})
  ON CREATE SET color.colorDesc = row.ColorDesc;

// Create varities
LOAD CSV WITH HEADERS FROM 'https://raw.githubusercontent.com/AlyshaHel/wine-engine/master/wine/data/variety_table.csv' AS row
MERGE (variety:Variety {varietyID: row.VarietyID})
  ON CREATE SET variety.varietyDesc = row.VarietyDesc;
