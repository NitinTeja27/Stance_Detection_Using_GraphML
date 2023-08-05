file_read = open('/content/stance_dataset_text.txt')
data_read = file_read.read()

file_write = open('/content/stance_dataset_text_new.txt','w')

string = ""
for item in data_read:
    if(item!='\n'):
        string+=item
    else:
        string+=','
        string+=item
        file_write.write(string)
        string = ""