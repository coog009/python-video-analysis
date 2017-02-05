#!/usr/bin/python

import sys
from videoparser import VideoParser as VideoParser
from filestream import FileReader as FileReader
from bitreader import BitReader as BitReader
from h264context import H264Context as H264Context
from h264context import H264Pps as H264Pps
from h264context import H264Sps as H264Sps
from globalconstant import Constant as Constant


class H264Parser(VideoParser):
    NALU_TYPE_NULL = 0
    NALU_TYPE_SLICE = 1
    NALU_TYPE_DPA = 2
    NALU_TYPE_DPB = 3
    NALU_TYPE_DPC = 4
    NALU_TYPE_IDR = 5
    NALU_TYPE_SEI = 6
    NALU_TYPE_SPS = 7
    NALU_TYPE_PPS = 8
    NALU_TYPE_AUD = 9
    NALU_TYPE_EOSEQ = 10
    NALU_TYPE_EOSTREAM = 11
    NALU_TYPE_FILL = 12
    NALU_TYPE_SPSEXT = 13
    NALU_TYPE_PREFIX = 14
    NALU_TYPE_SUB_SPS = 15
    NALU_TYPE_SLICE_AUX = 19
    NALU_TYPE_SLC_EXT = 20
    NALU_TYPE_VDRD = 24

    SLICESTATE_NONE = 0
    SLICESTATE_READNALU = 1
    SLICESTATE_PARSENALU = 2

    ZZ_SCAN = (0, 1, 4, 8, 5, 2, 3, 6, 9, 12, 13, 10, 7, 11, 14, 15)

    ZZ_SCAN8 = (0, 1, 8, 16, 9, 2, 3, 10, 17,
                24, 32, 25, 18, 11, 4, 5, 12,
                19, 26, 33, 40, 48, 41, 34, 27,
                20, 13, 6, 7, 14, 21, 28, 35,
                42, 49, 56, 57, 50, 43, 36, 29,
                22, 15, 23, 30, 37, 44, 51, 58,
                59, 52, 45, 38, 31, 39, 46, 53,
                60, 61, 54, 47, 55, 62, 63)

    def __init__(self):
        self.h264ctx = H264Context()
        self.next_state = H264Parser.SLICESTATE_NONE

    def parse_nalu_header(self):
        h264ctx = self.h264ctx
        fsreader = h264ctx.fsreader
        bitsreader = h264ctx.bitsreader
        nalu = h264ctx.cur_nalu.nalu
        value = [0]
        bitsreader.read_bits(1, value)
        nalu["forbidden_bit"] = value[0]
        if nalu["forbiden_bit"] == 0:
            return Constant.PVA_ERR_STREAM
        bitsreader.read_bits(2, value)
        nalu["nal_ref_idc"] = value[0]
        bitsreader.read_bits(5, value)
        nalu["nal_unit_type"] = value[0]
        cur_nalu.ualu_header_bytes = 1
        if nalu["nal_unit_type"] == H264Parser.NALU_TYPE_PREFIX or \
                nalu["nal_unit_type"] == NALU_TYPE_SLC_EXT:
            bitsreader.read_bits(1, value)
            nalu["svc_extension_flag"] = value[0]
            if nalu["svc_extension_flag"]:
                print "svc extension is not supported"
                return Constant.PVA_ERR_STREAM
            else:  # MVC
                mvc = nalu["mvc_ext"]
                bitsreader.read_bits(1, value)
                mvc["non_idr_flag"] = value[0]
                bitsreader.read_bits(6, value)
                mvc["priority_id"] = value[0]
                bitsreader.read_bits(10, value)
                mvc["view_id"] = value[0]
                bitsreader.read_bits(3, value)
                mvc["temporal_id"] = value[0]
                bitsreader.read_bits(1, value)
                mvc["anchor_pic_flag"] = value[0]
                bitsreader.read_bits(1, value)
                mvc["inter_view_flag"] = value[0]
                # reserve bit
                bitsreader.read_bits(1, value)
                bitsreader.skip_longbits(3 * 32)

    def parse_one_nalu(self):
        h264ctx = self.h264ctx
        fsreader = h264ctx.fsreader
        bitsreader = h264ctx.bitsreader
        cur_nalu = h264ctx.cur_nalu
        self.parse_nalu_header()
        if cur_nalu.nalu_type == H264Parser.NALU_TYPE_PPS:

    def parse_scaclinglist(self, scaling_list, length, default_list_flag):
        bitsreader = h264ctx.bitsreader
        delta_scale = [0]
        last_scale = 8
        next_scale = 8
        zz_scan = H264Parser.ZZ_SCAN8 if length > 16 else H264Parser.ZZ_SCAN
        use_default = 0
        for j in range(length):
            if next_scale:
                bitsreader.read_se(value)
            scanj = zz_scan[j]
            if next_scale:
                bitsreader.read_se(delta_scale)
                next_scale = (last_scale + delta_scale[0] + 256) % 256
                default_list_flag[0] = (scanj == 0 and next_scale == 0)
            scaling_list[scanj] = last_scale if next_scale == 0 else next_scale
            last_scale = scaling_list[scanj]

    def parse_pps(self):
        h264ctx = self.h264ctx
        fsreader = h264ctx.fsreader
        bitsreader = h264ctx.bitsreader
        pps = H264Pps()
        value = [0]
        bitsreader.read_ue(value)
        pps["pic_parameter_set_id"] = value[0]
        bitsreader.read_ue(value)
        pps["seq_parameter_set_id"] = value[0]
        sps = h264ctx.sps_list[pps["seq_parameter_set_id"]]
        if pps["seq_parameter_set_id"] < 0 or \
                pps["seq_parameter_set_id"] > 32:
            pps["seq_parameter_set_id"] = 0
        if pps["pic_parameter_set_id"] < 0 or \
                pps["pic_parameter_set_id"] > 256:
            pps["pic_parameter_set_id"] = 0
        bitsreader.read_bits(1, value)
        pps["entropy_coding_mode_flag"] = value[0]
        bitsreader.read_bits(1, value)
        pps["bottom_field_pic_order_in_frame_present_flag"] = value[0]
        bitsreader.read_ue(value)
        pps["num_slice_groups_minus1"] = value[0]
        if pps["num_slice_groups_minus1"] > 0:
            bitsreader.read_ue(value)
            pps["slice_group_map_type"] = value[0]
            if pps["slice_group_map_type"] == 0:
                for i in range(pps["num_slice_groups_minus1"] + 1):
                    bitsreader.read_ue(value)
                    pps["run_length_minus1"][i] = value[0]
            elif pps["slice_group_map_type"] == 2:
                for i in range(pps["num_slice_groups_minus1"] + 1):
                    bitsreader.read_ue(value)
                    pps["top_left"] = value[0]
                    pps["bottom_right"] = value[0]
            elif pps["slice_group_map_type"] == 3 or \
                pps["slice_group_map_type"] == 4 or \
                    pps["slice_group_map_type"] == 5:
                bitsreader.read_bits(1, value)
                pps["slice_group_change_direct_flag"] = value[0]
                bitsreader.read_ue(value)
                pps["slice_group_change_rate_minus1"] = value[0]
            elif pps["slice_group_map_type"] == 6:
                bitsreader.read_ue(value)
                pps["pic_size_in_map_units_minus1"] = value[0]
                for i in range(pps["pic_size_in_map_units_minus1"] + 1):
                    bitsreader.read_bits(1, value)
                    pps["slice_group_id"][i] = value[0]
        bitsreader.read_ue(value)
        pps["num_ref_idx_l0_default_active_minus1"] = value[0]
        bitsreader.read_ue(value)
        pps["num_ref_idx_l1_default_active_minus1"] = value[0]
        bitsreader.read_bits(1, value)
        pps["weighted_pred_flag"] = value[0]
        bitsreader.read_bits(2, value)
        pps["weighted_bipred_idc"] = value[0]
        bitsreader.read_se(value)
        pps["pic_init_qp_minus26"] = value[0]
        bitsreader.read_se(value)
        pps["pic_init_qs_minus26"] = value[0]
        bitsreader.read_se(value)
        pps["chroma_qp_index_offset"] = value[0]
        bitsreader.read_bits(1, value)
        pps["deblocking_filter_control_present_flag"] = value[0]
        bitsreader.read_bits(1, value)
        pps["constrained_intra_pred_flag"] = value[0]
        bitsreader.read_bits(1, value)
        pps["redundant_pic_cnt_present_flag"] = value[0]
        if bitsreader.has_more_rbsp_data():
            bitsreader.read_bits(1, value)
            pps["transform_8x8_mode_flag"] = value[0]
            bitsreader.read_bits(1, value)
            pps["pic_scaling_matrix_present_flag"] = value[0]
            if pps["pic_scaling_list_present_flag"]:
                for i in range((2 if sps["chroma_format_idc"] != 3 else 6)
                               * pps["transform_8x8_mode_flag"] + 6):
                    bitsreader.read_bits(1, value)
                    pps["pic_scaling_list_present_flag"][i] = value[0]
                    if pps["pic_scaling_list_present_flag"][i]:
                        if i < 6:
                            parse_scaclinglist(pps["scaling_list_4x4"][i],
                                               16,
                                               value)
                            pps["use_default_scaling_matrix_4x4_flag"] = value[
                                0]
                        else:
                            parse_scaclinglist(pps["scaling_list_8x8"][i - 6],
                                               64,
                                               value)
                            pps["use_default_scaling_matrix_8x8_flag"] = value[
                                0]
            bitsreader.read_se(value)
            pps["second_chroma_qp_index_offset"] = value[0]
        h264ctx.cur_pps = pps

    def parse_vui(self, vui):
        bitsreader = h264ctx.bitsreader

        

    def parse_sps(self):
        h264ctx = self.h264ctx
        bitsreader = h264ctx.bitsreader
        sps = H264Sps()
        value = [0]
        bitsreader.read_bits(8, value)
        sps["profile_idc"] = value[0]
        bitsreader.read_bits(1, value)
        sps["constrained_set0_flag"] = value[0]
        bitsreader.read_bits(1, value)
        sps["constrained_set1_flag"] = value[0]
        bitsreader.read_bits(1, value)
        sps["constrained_set2_flag"] = value[0]
        bitsreader.read_bits(1, value)
        sps["constrained_set3_flag"] = value[0]
        bitsreader.read_bits(1, value)
        sps["constrained_set4_flag"] = value[0]
        bitsreader.read_bits(1, value)
        sps["constrained_set5_flag"] = value[0]
        bitsreader.read_bits(2, value)
        bitsreader.read_bits(8, value)
        sps["level_idc"] = value[0]
        bitsreader.read_ue(value)
        sps["seq_parameter_set_id"] = value[0]
        if sps["profile_idc"] == 100 or sps["profile_idc"] == 110 or \
            sps["profile_idc"] == 122 or sps["profile_idc"] == 244 or \
            sps["profile_idc"] == 44 or sps["profile_idc"] == 83 or \
            sps["profile_idc"] == 86 or sps["profile_idc"] == 118 or \
            sps["profile_idc"] == 128 or sps["profile_idc"] == 138 or \
                sps["profile_idc"] == 139 or sps["profile_idc"] == 134:
            bitsreader.read_ue(value)
            sps["chroma_format_idc"] = value[0]
            if sps["chroma_format_idc"] == 3:
                bitsreader.read_bits(1, value)
                sps["separate_colour_plane_flag"] = value[0]
            bitsreader.read_ue(value)
            sps["bit_depth_luma_minus8"] = value[0]
            bitsreader.read_ue(value)
            sps["bit_depth_chroma_minus8"] = value[0]
            bitsreader.read_bits(1, value)
            sps["qpprime_y_zero_transform_bypass_flag"] = value[0]
            bitsreader.read_bits(1, value)
            sps["seq_scaling_matrix_present_flag"] = value[0]
            if sps["seq_scaling_matrix_present_flag"]:
                for i in range(8 if sps["chroma_format_idc"] != 3 else 12):
                    bitsreader.read_bits(1, value)
                    sps["seq_scaling_list_present_flag"][i] = value[0]
                    if sps["seq_scaling_list_present_flag"][i]:
                        if i < 6:
                            parse_scaclinglist(sps["scaling_list_4x4"][i],
                                               16,
                                               value)
                            sps["use_default_scaling_matrix_4x4_flag"][i] = value[0]
                        else:
                            parse_scaclinglist(sps["scaling_list_8x8"][i],
                                               64,
                                               value)
                            sps["use_default_scaling_matrix_8x8_flag"][i] = value[0]
            bitsreader.read_ue(value)
            sps["log2_max_frame_num_minus4"] = value[0]
            bitsreader.read_ue(value)
            sps["pic_order_cnt_type"] = value[0]
            if sps["pic_order_cnt_type"] == 0:
                bitsreader.read_ue(value)
                sps["log2_max_pic_order_cnt_lsb_minus4"] = value[0]
            elif sps["pic_order_cnt_type"] == 1:
                bitsreader.read_bits(1, value)
                sps["delta_pic_order_always_zero_flag"] = value[0]
                bitsreader.read_se(value)
                sps["offset_for_non_ref_pic"] = value[0]
                bitsreader.read_se(value)
                sps["offset_for_top_to_bottom_field"] = value[0]
                bitsreader.read_ue(value)
                sps["num_ref_frames_in_pic_order_cnt_cycle"] = value[0]
                for i in range(sps["num_ref_frames_in_pic_order_cnt_cycle"]):
                    bitsreader.read_se(value)
                    sps["offset_for_ref_frame"][i] = value[0]
            bitsreader.read_ue(value)
            sps["max_num_ref_frame"] = value[0]
            bitsreader.read_bits(1, value)
            sps["gaps_in_frame_num_value_allowed_flag"] = value[0]
            bitsreader.read_ue(value)
            sps["pic_width_in_mbs_minus1"] = value[0]
            bitsreader.read_ue(value)
            sps["pic_height_in_map_units_minus1"] = value[0]
            bitsreader.read_bits(1, value)
            sps["frame_mbs_only_flag"] = value[0]
            if sps["frame_mbs_only_flag"] == 0:
                bitsreader.read_bits(1, value)
                sps["mb_adaptive_frame_field_flag"] = value[0]
            bitsreader.read_bits(1, value)
            sps["direct_8x8_inference_flag"] = value[0]
            bitsreader.read_bits(1, value)
            sps["frame_cropping_flag"] = value[0]
            if sps["frame_cropping_flag"]:
                bitsreader.read_ue(value)
                sps["frame_crop_left_offset"] = value[0]
                bitsreader.read_ue(value)
                sps["frame_crop_right_offset"] = value[0]
                bitsreader.read_ue(value)
                sps["frame_crop_top_offset"] = value[0]
                bitsreader.read_ue(value)
                sps["frame_crop_bottom_offset"] = value[0]
            bitsreader.read_bits(1, value)
            sps["vui_parameters_present_flag"] = value[0]
            if sps["vui_parameters_present_flag"]:
                parse_vui_parameters(sps["vui"])

    def parse_loop(self):
        h264ctx = self.h264ctx
        fsreader = h264ctx.fsreader
        bitsreader = h264ctx.bitsreader
        frame = h264ctx.frame


def main():
    parser = H264Parser()
    print "input argv ", len(sys.argv)
    if len(sys.argv) <= 1:
        parser.usage()
        sys.exit(1)
    parser.parse_options(sys.argv)
    parser.h264ctx.fsreader = FileReader(parser.input_name, "rb")
    parser.h264ctx.frame.buffer = parser.h264ctx.fsreader.get_one_frame()
    parser.h264ctx.bitsreader = BitReader(parser.h264ctx.frame.buffer)
    parser.h264ctx.bitsreader.set_pre_detection()

    # skip 0x00000001
    parser.h264ctx.bitreader.skip_longbits(32)
    forbiden = [0]
    parser.h264ctx.bitreader.read_bits(1, forbiden)
    value = [0]
    bitsreader.skip_longbits(32)
    bitsreader.read_bits(4, value)
    print value[0]
    bitsreader.read_bits(2, value)
    print value[0]
    bitsreader.read_bits(2, value)
    print value[0]
    bitsreader.read_bits(8, value)
    print value[0]
    bitsreader.read_ue(value)
    print value[0]
    del fsreader

if __name__ == "__main__":
    main()
