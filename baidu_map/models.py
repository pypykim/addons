# -*- coding: utf-8 -*-
import openerp
from openerp import models, fields, api
import werkzeug


def urlplus(url, params):
    return werkzeug.Href(url)(params or None)


class res_partner(models.Model):
    _inherit = "res.partner"

    @api.model
    def baidu_map_img(self, zoom=10, width=298, height=298):
        '''
        http://api.map.baidu.com/staticimage?center=116.403874,39.914888&width=300&height=200&zoom=11

        '''

        params = {
            'center': '%s,%s' % (str(self.partner_longitude), str(self.partner_latitude)),
            'width': "%s" % (width),
            'height': "%s" % (height),
            'markers': '%s,%s' % (str(self.partner_longitude), str(self.partner_latitude)),
            'markerStyles': '1,0',
            'zoom': zoom,
        }
        return urlplus('http://api.map.baidu.com/staticimage', params)

    @api.model
    def baidu_map_link(self, zoom=10):
        '''
     http://api.map.baidu.com/marker?location=40.047669,116.313082&title=我的位置&content=百度奎科大厦&output=html&src=yourComponyName|yourAppName    //调起百度PC或web地图，且在（lat:39.916979519873，lng:116.41004950566）坐标点上显示名称"我的位置"，内容"百度奎科大厦"的信息窗口。
        '''
        params = {
            'location': '%s,%s' % (str(self.partner_longitude), str(self.partner_latitude)),
            'title': "%s" % (self.name),
            'content': "%s" % (self.name),
            'output': 'html',
            'src': self.name,
            'zoom': zoom,
        }
        return urlplus('http://api.map.baidu.com/marker', params)


class res_company(models.Model):
    _inherit = "res.company"

    @api.model
    def baidu_map_img(self, zoom=15, width=298, height=298):
        return self.partner_id.baidu_map_img(zoom, width, height) or None

    @api.model
    def baidu_map_link(self, zoom=10):
        return self.partner_id.baidu_map_link(zoom) or None
