# DATtoGeoJSON

A simple Python-based FAA DAT to GeoJSON Converter for use with CRC.

## Format Note

CRC uses EPSG:4326 format for points. Many online GeoJSON viewers, such as [GeoJSON.io](https://geojson.io/), use different formats that place the Longitude first. For this reason, if you test the default output of this script in many of those resources, it will not render properly. If you would like to render a test output, use the `--test` flag.

## Limitations

The DAT files that I was provided assume that coordinates are N Lat and W Lon, so the W coordinates are positive. This will not work for facilities at/near the antimeridian until I can see how that case is handled in DAT files from that area.

## Requirements

Python3.8 or Later (Tested with Python 3.9.13)

Only imports are Argparse, CSV, Math, and OS, so it should run on a standard Python implementation.

## Instructions for use

To process files for a single facility:

1. Place the DAT files in the `dat_source` directory.
2. Run the following command:
   <br/>
   ```
   python3 convert.py [--radius X (default 140)]
   ```

To process multiple facilities at once:

1. Create folders for each facility in the `dat_source` directory.
2. Place the DAT files for each facility in their respective facility folders.
   <br/>**Note:** The script will use the file names as the export name (e.g. `/dat_source/IAD/Base.dat` will be saved as `/output/IAD_Base.geojson`)
   <br/><br/><img src="./resources/facilities.jpg" alt="Folder Structure" width="200"/>
3. Run the following command:
   <br/>
   ```
   python3 convert.py [--radius X (default 140)]
   ```

### Optional Command Line Arguments

The optional `--radius X` argument is provided because the DAT files include everything that is also shown in the PDF accompanying the DAT file, to include the border and text at the bottom left and right. This border is generally around 150NM from the center point (point of tangency) declared in the file, and there is a radial line showing MAG versus TRUE that extends inside of the border, necessitating a radius smaller than the border itself. The radius may be smaller for smaller TRACONS or Towers, so the default of 140 can be overridden by passing `--radius X`, where `XX` is an integer representing the NM from the center of the map.
<br/>Example: `python3 convert.py --radius 50`
<br/>

<p align="center">
<img src="./resources/border.jpg" alt="Folder Structure" width="400"/>
</p>

If you have a set of files where you wish to provide per-file overrides, the `--filelist` argument is available to facilitate that. Please follow these instructions carefully:

1. Run the script with the `--filelist` flag:
   ```
   python3 convert.py --filelist
   ```
2. Find the FileList.csv file in the `output` folder.
3. Open the FileList.csv in a spreadsheet program (Excel, Numbers, etc.), or better, a text editor if you are familiar enough with raw CSV.
   <br/>**Note:** Do not alter the headers, or the data in the first column (Source).
4. Provide override data:
   - Optional: Range must be an integer or blank.
   - Optional: OutputFileName must be a string or blank.
   - Optional: CenterPointLat and CenterPointLon must both be present as decimal Lat/Lons, and the Lon must be positive.
     <br/>**Note:** The FAA format assumes west lons are positive in the DAT files.
5. Save the override data in the FileList.csv.
6. Run the script with the `--readfile` flag:
   ```
   python3 convert.py --readfile
   ```

**Note:** The script will try to make sense of the values as best that it can. If the program editing the CSV adds odd formatting, it could cause odd results. If files are missing from the export, or ranges are not being set to the override values, it is likely because it did not understand the data in the field (data unable to be parsed into an int or float gets silently ignored at the moment).

# Contributions

Want to contribute? Check out the [Open Issues](https://github.com/misterrodg/DATtoGeoJSON/issues), fork, and open a [Pull Request](https://github.com/misterrodg/DATtoGeoJSON/pulls).

Additional contributors will be listed here.

# License

This is licensed under [GPL 3.0](./LICENSE).
