from . import detect_faces, detect_lps, render_pano, detect_faces_dlib, blur_regions, detect_flipped_profiles

workers = [
    blur_regions.BlurRegions,
    detect_flipped_profiles.DetectProfiles,
    detect_faces_dlib.DetectFacesDlib,
    detect_lps.DetectLicensePlates,
    detect_faces.DetectFaces,
    render_pano.RenderPano
]
