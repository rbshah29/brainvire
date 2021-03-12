from odoo import models,fields,api
from odoo.osv import expression
from lxml import etree

class ProductBrand(models.Model):
	_name = "productbrand"
	_rec_name = "brand_name"

	brand_name = fields.Char(required=True)
	brand_code = fields.Char(required=True)

class ProductExtends(models.Model):
	_inherit = 'product.product'
 
	brand_id = fields.Many2one('productbrand')

	####name search method 
	@api.model
	def _name_search(self, name , args=None, operator="ilike",limit=100,name_get_uid=None):
		context = self.env.context
		args = args or []
		domain = []
		if args is None:
			args=[]
		else:
			if context.get('part_id'):
				domain=[('brand_id','=',context.get('part_id'))]				
				# print("___________--------_________________--------_________-------_______-------______---")
				return self._search(expression.AND([domain,args]),limit=limit)

			else:
				print("_________---**********")
				return self._search(expression.AND([domain,args]),limit=limit)
		return self._search(expression.AND([domain,args]),limit=limit)


class SaleExtend(models.Model):
	_inherit = 'sale.order'


	brand_ids = fields.Many2one('productbrand')

	#FIELDS VIEW GET METHOD TO MAKE FIELDS REQUIRED

	@api.model
	def _fields_view_get(self, view_id=None, view_type=False, toolbar=False, submenu=False):
		res = super(SaleExtend, self)._fields_view_get(view_id=view_id, view_type=view_type,toolbar=toolbar, submenu=False)
		doc = etree.XML(res['arch'])
		for node in doc.xpath("//field[@name='brand_ids']"):
			node.set('required', '1')
		res['arch'] = etree.tostring(doc)
		return res




#NAME GET METHOD TO GET CUST. NUMBER AND CUST. NAME TOGETHER IN SALE MODULE 
class Inherit(models.Model):
	_inherit = 'res.partner'
	def name_get(self):
		res = []
		for rec in self:
			print("----====----====\n\n\n\n\n")
			if rec.phone:
				res.append((rec.id, '%s  %s' % (rec.name, rec.phone)))
			if not rec.phone:
				res.append((rec.id,' %s ' % (rec.name)))
			# rec.phone(value = "None")
		return res	