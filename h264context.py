#!/usr/bin/python


class H264Hrd:

    def __init__(self):
        self.hrd = {"cpb_cnt_minus1": 0,
                    "bit_rate_scale": 0,
                    "cpb_size_scale": 0,
                    "bit_rate_value_minus1": [0] * 32,
                    "cpb_size_value_minus1": [0] * 32,
                    "cbr_flag": [0] * 32,
                    "initial_cpb_removal_delay_length_minus1": 0,
                    "cpb_removal_delay_length_minus1": 0,
                    "dpb_output_delay_length_minus1": 0,
                    "time_offset_lenght": 0}


class H264Vui:

    def __init__(self):
        self.vui = {"aspect_ratio_info_present_flag:": 0,
                    "aspect_ratio_idc": 0,
                    "sar_width": 0,
                    "sar_height": 0,
                    "overscan_info_present_flag": 0,
                    "overscan_appropriate_flag": 0,
                    "video_signal_type_present_flag": 0,
                    "video_format": 0,
                    "video_full_range_flag": 0,
                    "colour_description_present_flag": 0,
                    "colour_primaries": 0,
                    "transfer_characteristics": 0,
                    "matrix_coefficients": 0,
                    "chroma_location_info_present_flag": 0,
                    "chroma_sample_loc_type_top_field": 0,
                    "chroma_sample_loc_type_bottom_field": 0,
                    "timing_info_present_flag": 0,
                    "num_units_in_tick": 0,
                    "time_scale": 0,
                    "fixed_frame_rate_flag": 0,
                    "nal_hrd_parameters_present_flag": 0,
                    "nal_hrd_parameters": H264Hrd(),
                    "vcl_hrd_parameters_present_flag": 0,
                    "vcl_hrd_parameters": H264Hrd(),
                    "low_delay_hrd_flag": 0,
                    "pic_struct_present_flag": 0,
                    "bitstream_restriction_flag": 0,
                    "motion_vectors_over_pic_boundaries_flag": 0,
                    "max_bytes_per_pic_denom": 0,
                    "max_bits_per_mb_denom": 0,
                    "log2_max_mv_length_vertical": 0,
                    "log2_max_mv_length_horizontal": 0,
                    "num_reorder_frames": 0,
                    "max_dec_frame_buffering": 0}


class H264Sps:

    def __init__(self):
        self.sps = {"valid": 0,
                    "profile_idc": 0,
                    "constrained_set0_flag": 0,
                    "constrained_set1_flag": 0,
                    "constrained_set3_flag": 0,
                    "constrained_set4_flag": 0,
                    "constrained_set5_flag": 0,
                    "level_idc": 0,
                    "seq_parameter_set_id": 0,
                    "chroma_format_idc": 0,
                    "separate_colour_plane_flag": 0,
                    "bit_depth_luma_minus8": 0,
                    "bit_depth_chroma_minus8": 0,
                    "qpprime_y_zero_transform_bypass_flag": 0,
                    "seq_scaling_matrix_present_flag": 0,
                    "seq_scaling_list_present_flag": [0] * 12,
                    "scaling_list_4x4": [([0] * 16) for i in range(6)],
                    "use_default_scaling_matrix_4x4_flag": [0] * 6,
                    "scaling_list_8x8": [([0] * 64) for i in range(6)],
                    "use_default_scaling_matrix_8x8_flag": [0] * 6,
                    "log2_max_frame_num_minus4": 0,
                    "pic_order_cnt_type": 0,
                    "log2_max_pic_order_cnt_lsb_minus4": 0,
                    "delta_pic_order_always_zero_flag": 0
                    "offset_for_non_ref_pic": 0,
                    "offset_for_top_to_bottom_field": 0,
                    "num_ref_frames_in_pic_order_cnt_cycle": 0,
                    "offset_for_ref_frame": [0] * 256,
                    "max_num_ref_frames": 0,
                    "gaps_in_frame_num_value_allowed_flag": 0,
                    "pic_width_in_mbs_minus1": 0,
                    "pic_height_in_map_units_minus1": 0,
                    "frame_mbs_only_flag": 0,
                    "mb_adaptive_frame_field_flag": 0,
                    "direct_8x8_inference_flag": 0,
                    "frame_crop_left_offset": 0,
                    "frame_crop_right_offset": 0,
                    "frame_crop_top_offset": 0,
                    "frame_crop_bottom_offset": 0,
                    "vui_parameters_present_flag": 0,
                    "vui": H264Vui()}


class H264Pps:

    def __init__(self):
        self.pps = {"valid:"0,
                    "pic_parameter_set_id": 0,
                    "seq_parameter_set_id": 0,
                    "entropy_coding_mode_flag": 0
                    "bottom_field_pic_order_in_frame_present_flag": 0,
                    "num_slice_groups_minus1": 0,
                    "slice_group_map_type": 0,
                    "run_length_minus1": [0] * 8,
                    "top_left": [0] * 8,
                    "bottom_right": [0] * 8,
                    "slice_group_change_direction_flag": 0,
                    "slice_group_change_rate_minus1": 0,
                    "pic_size_in_map_units_minus1": 0,
                    "slice_group_id": [0] * 8,
                    "num_ref_idx_l0_default_active_minus1": 0,
                    "num_ref_idx_l1_default_active_minus1": 0,
                    "weighted_pred_flag": 0,
                    "weighted_bipred_idc": 0,
                    "pic_init_qp_minus26": 0,
                    "pic_init_qs_minus26": 0,
                    "chroma_qp_index_offset": 0,
                    "deblocking_filter_control_present_flag": 0,
                    "constrained_intra_pred_flag": 0,
                    "redundant_pic_cnt_present_flag": 0,
                    "transform_8x8_mode_flag": 0,
                    "pic_scaling_matrix_present_flag": 0,
                    "pic_scaling_list_present_flag": [0] * 12,
                    "scaling_list_4x4": [([0] * 16) for i in range(6)],
                    "use_default_scaling_matrix_4x4_flag": [0] * 6,
                    "scaling_list_8x8": [([0] * 64) for i in range(6)],
                    "use_default_scaling_matrix_8x8_flag": [0] * 6,
                    "second_chroma_qp_index_offset": 0}


class H264NalSvcExt:

    def __init__(self):
        self.ext = {"idr_flag": 0,
                    "priority_id": 0,
                    "no_inter_layaer_pred_flag": 0,
                    "dependency_id": 0,
                    "quality_id": 0,
                    "temporal_id": 0,
                    "use_ref_base_pic_flag": 0,
                    "discardable_flag": 0,
                    "output_flag": 0}


class H264Nal3DavcExt:

    def __init__(self):
        self.ext = {"view_idx": 0,
                    "depth_flag": 0,
                    "non_idr_flag": 0,
                    "temporal_id": 0,
                    "anchor_pic_flag": 0,
                    "inter_view_flag": 0}


class H264MvcExt:

    def __init__(self):
        self.ext = {"non_idr_flag": 0,
                    "priority_id": 0,
                    "view_id": 0,
                    "temporal_id": 0,
                    "anchor_pic_flag": 0,
                    "inter_view_flag": 0}


class H264Nalu:

    def __init__(self):
        self.nalu = {"forbidden_zero_bit": 0,
                     "nal_ref_idc": 0,
                     "nal_unit_type": 0,
                     "svc_extension_flag": 0,
                     "avc_3d_extension_flag": 0,
                     "svc_ext": H264NalSvcExt(),
                     "3davc_ext": H264Nal3DavcExt(),
                     "mvc_ext": H264MvcExt()}


class PVAFrame:

    def __init__(self):
        self.buffer = []
        self.size = 0


class H264Context:

    def __init__(self):
        self.sps_list = [H264Sps()] * 32
        self.cur_sps = H264Sps()
        self.pps_list = [H264Pps()] * 256 
        self.cur_pps = H264Pps()
        self.cur_nalu = H264Nalu()
        # BitReader
        self.bitsreader = 0
        # FileReader
        self.fsreader = 0
        self.frame = PVAFrame()
