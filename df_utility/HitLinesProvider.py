from geom_classes.Line import Line
from geom_classes.GlobalZTranslation import GlobalZTranslation


def get_current_hits_df(event_id, group_id, hits_df):
    return hits_df.loc[(hits_df['eventID'] == event_id) & (hits_df['groupID'] == group_id)]


def get_det_geom_info(det_id, geom_df):
    return geom_df.loc[(geom_df['detId'] == det_id)].iloc[0]


def get_lines_from_hits_df(hits_df, geom_df):
    lines = []

    for idx, row in hits_df.iterrows():
        position = row['position']
        det_id = 10 * row['rpID'] + row['siliconID']
        det_info = get_det_geom_info(det_id, geom_df)

        x = det_info['x'] + position * det_info['dx']
        y = det_info['y'] + position * det_info['dy']
        z = det_info['z']
        dx = - det_info['dy']
        dy = det_info['dx']
        dz = 0.0

        lines.append(Line(x, y, z, dx, dy, dz, det_id=det_id))

    return lines


def apply_transformations(hit_lines, translate_first_z_to_zero, in_mm):

    if in_mm:
        for line in hit_lines:
            line.z = line.z * 1000

    if translate_first_z_to_zero:
        GlobalZTranslation.FIRST_DET_Z_IN_MM = min([line.z for line in hit_lines], key=abs)

        for line in hit_lines:
            line.z = line.z - GlobalZTranslation.FIRST_DET_Z_IN_MM


def extract_hit_lines(hits_df, geom_df, eventID, groupID, translate_first_z_to_zero=True, in_mm=True):
    current_hits_df = get_current_hits_df(eventID, groupID, hits_df)
    hit_lines = get_lines_from_hits_df(current_hits_df, geom_df)
    apply_transformations(hit_lines, translate_first_z_to_zero, in_mm)

    return hit_lines