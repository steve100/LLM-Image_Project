import exiftool
et = exiftool.ExifTool()
print(hasattr(et, 'get_metadata_batch'))  # Should print: True

