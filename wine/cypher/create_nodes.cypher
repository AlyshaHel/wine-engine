//MATCH (n) DETACH DELETE n

// Create wines
LOAD CSV WITH HEADERS FROM 'https://raw.githubusercontent.com/AlyshaHel/wine-engine/master/wine/data/winename_table.csv' AS row
MERGE (wine:Wine {wineID: row.WineID})
  ON CREATE SET wine.wineDesc = row.WineDesc, wine.vintage = toInteger(row.Vintage);
MATCH (n:Wine) RETURN n LIMIT 25

// Create descriptors
LOAD CSV WITH HEADERS FROM 'https://raw.githubusercontent.com/AlyshaHel/wine-engine/master/wine/data/descriptor_table.csv' AS row
MERGE (descriptor:Descriptor {descriptorID: row.DescriptorID})
  ON CREATE SET descriptor.descriptorDesc = row.DescriptorDesc;
MATCH (n:Descriptor) RETURN n LIMIT 25

// Create colors
LOAD CSV WITH HEADERS FROM 'https://raw.githubusercontent.com/AlyshaHel/wine-engine/master/wine/data/color_table.csv' AS row
MERGE (color:Color {colorID: row.ColorID})
  ON CREATE SET color.colorDesc = row.ColorDesc;
MATCH (n:Color) RETURN n LIMIT 25

// Relate descriptors to wine
LOAD CSV WITH HEADERS FROM "https://raw.githubusercontent.com/AlyshaHel/wine-engine/master/wine/data/descriptor_relationships_table.csv" AS row
MATCH (descriptor:Descriptor {descriptorID: row.DescriptorID})
MATCH (wine:Wine {wineID: row.WineID})
MERGE (wine)-[:HAS_DESC]->(descriptor);

// Relate colors to wine
LOAD CSV WITH HEADERS FROM 'https://raw.githubusercontent.com/AlyshaHel/wine-engine/master/wine/data/color_relationships_table.csv' AS row
MATCH (color:Color {colorID: row.ColorID})
MATCH (wine:Wine {wineID: row.WineID})
MERGE (wine)-[:HAS_COLOR]->(color)
