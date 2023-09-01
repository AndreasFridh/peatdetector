# Peat Detector

#Flask Routes:
/run_analysis: Runs the peat detector and returns a JSON object with the analysis.
/get_img: Grabs a frame from the camera and returns it as an image file.
/get_img_masked: Grabs a masked frame from the camera and returns it.
/get_last_img: Returns the last image captured.
/get_mask: Returns the mask applied to the image.
/generate_report: Generates a report based on the last analysis.
/exp_show, /exp_dec, /exp_inc, /exp_auto, /exp_set: Various routes for manipulating and fetching the camera's exposure settings.

#Class Definitions:
AnalysisResponse: This class is used to hold the results of an image analysis.

blobs_found: Boolean indicating if blobs were found in the image.
largest_blob_size: Size of the largest blob found.
largest_blob_pos_x: X-position of the largest blob.
largest_blob_pos_y: Y-position of the largest blob.
exposure_time: Camera's exposure time.
Images: Holds different processed states of an image.

raw: Raw image.
bw: Black and white image.
mask: Mask applied to the image.
masked: Image after mask application.
analyzed: Image after analysis.
filtered: Image after filtering.