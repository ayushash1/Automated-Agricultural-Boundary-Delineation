import ee

def mask_s2_clouds(image):
    """
    Masks clouds in Sentinel-2 imagery using the QA60 band.
    Matches 'Cloud & Shadow Masking (QA60 Band)' in Zone 1.
    """
    qa = image.select('QA60')

    # Bits 10 and 11 are clouds and cirrus, respectively
    # 1 << 10 creates a bitmask where only the 10th bit is 1
    cloud_bit_mask = 1 << 10
    cirrus_bit_mask = 1 << 11

    # Both flags should be set to zero, indicating clear conditions
    mask = qa.bitwiseAnd(cloud_bit_mask).eq(0) \
             .And(qa.bitwiseAnd(cirrus_bit_mask).eq(0))

    # Return the image with the mask applied and scaled to reflectance (0-1)
    # Note: divide(10000) is standard for Sentinel-2 SR data
    return image.updateMask(mask).divide(10000)

def get_clean_collection(aoi, start_date, end_date):
    """
    Filters the Sentinel-2 collection and applies the cloud mask.
    """
    collection = (ee.ImageCollection("COPERNICUS/S2_SR_HARMONIZED")
                  .filterBounds(aoi)
                  .filterDate(start_date, end_date)
                  # Pre-filter for overall cloudy scenes to save processing time
                  .filter(ee.Filter.lt('CLOUDY_PIXEL_PERCENTAGE', 20))
                  .map(mask_s2_clouds))
    
    return collection