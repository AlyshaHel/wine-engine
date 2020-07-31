//MATCH (n) DETACH DELETE n

// Relate descriptors to wine
LOAD CSV WITH HEADERS FROM "https://raw.githubusercontent.com/AlyshaHel/wine-engine/master/wine/data/descriptor_relationships_table.csv" AS row
MATCH (descriptor:Descriptor {descriptorID: row.DescriptorID})
MATCH (wine:Wine {wineID: row.WineID})
MERGE (wine)-[:HAS_DESC]->(descriptor);

// Relate colors to wine
LOAD CSV WITH HEADERS FROM 'https://raw.githubusercontent.com/AlyshaHel/wine-engine/master/wine/data/color_relationships_table.csv' AS row
MATCH (color:Color {colorID: row.ColorID})
MATCH (wine:Wine {wineID: row.WineID})
MERGE (wine)-[:HAS_COLOR]->(color);

// Relate variety to wine
LOAD CSV WITH HEADERS FROM 'https://raw.githubusercontent.com/AlyshaHel/wine-engine/master/wine/data/variety_relationships_table.csv' AS row
MATCH (variety:Variety {varietyID: row.VarietyID})
MATCH (wine:Wine {wineID: row.WineID})
MERGE (wine)-[:IS_VARIETY]->(variety);
