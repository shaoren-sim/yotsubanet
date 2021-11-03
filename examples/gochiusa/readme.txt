This example shows how to handle cases where romanization of the character names result in different English names depending on the translation. 

For example, "理世" is romanized as "Rize" or "Rise", and "紗路" is romanized as "Sharo" and "Syaro".

For the webscraper, we can define different romanized names as two distinct classes, and merge them in-post. As long as the dataset cleanup pass is done once again post-merging, the dataset will be usable.