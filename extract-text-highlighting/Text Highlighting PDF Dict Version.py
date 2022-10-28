# Finding all of highlighted text from pdf using pdfplumber

import pdfplumber

pdf = pdfplumber.open("/Users/mazz/Documents/Programming/Python/NLP/data/Highlighting Example 5.pdf")
n = len(pdf.pages)

# creating a dictionary of pages
p = {}

for i in range(n):
    key = i
    p[key] = pdf.pages[i]

highlights = {}


# loop over all the pages in the file
for i in range(n):
    # move to page i
    page = p[i]
    # make a list for the given page
    annots = []
    # iterate through all the annotations
    #print(len(page.annots))
    for annotation in page.annots: # a problem with .annot is that it takes in urls and emails (anything that is clickable inside the pdf)
        # annotation is a dictionary containing `x0`, `x1`, `y0`, `y1`
        if annotation['uri'] == None: # make sure that annottion is not due to it being a url
            #print(annotation)
            #heigh_of_letters = (page.height - annotation['y0']) - (page.height - annotation['y1'])
            #print("height = ", heigh_of_letters)
            bbox = (annotation['x0'] + 4, page.height - annotation['y1'], annotation['x1'] - 4, page.height - annotation['y0'])
            #print(bbox)
            #bbox = (0, 0, page.width, page.height)
            temp_high_page = page.crop(bbox=bbox, strict=False, relative=False)
            temp_high_text = temp_high_page.extract_text()
            if temp_high_text != '':
                annots.append(temp_high_text) # second tuple entry will help determine if the text is on the same line
    if annots != []:
        highlights[i+1] = annots

final_result = highlights


print(final_result)