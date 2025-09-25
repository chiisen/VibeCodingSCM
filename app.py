from flask import Flask, render_template, request, redirect, url_for, flash
from datetime import datetime
import os

app = Flask(__name__)
app.secret_key = 'dev-secret-key-change-in-production'

# 静态初始数据
SUPPLIERS = [
    {
        'id': 1,
        'name': 'ABC 电子供应商',
        'contact': '张三',
        'phone': '138-0000-0001',
        'address': '北京市朝阳区',
        'products': '电子元件、芯片'
    },
    {
        'id': 2,
        'name': 'XYZ 物流公司',
        'contact': '李四',
        'phone': '138-0000-0002',
        'address': '上海市浦东新区',
        'products': '包装材料、配件'
    }
]

LOGISTICS = [
    {
        'id': 1,
        'order_id': 'L001',
        'supplier_id': 1,
        'destination': '北京市海淀区仓库',
        'status': '待出货',
        'created_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }
]

INVENTORY = [
    {
        'id': 1,
        'name': '电子元件A',
        'quantity': 1000,
        'min_threshold': 100,
        'supplier_id': 1
    },
    {
        'id': 2,
        'name': '包装材料B',
        'quantity': 500,
        'min_threshold': 50,
        'supplier_id': 2
    }
]

DELIVERY = [
    {
        'id': 1,
        'order_id': 'D001',
        'customer': '客户A',
        'address': '北京市西城区',
        'status': '准备中',
        'created_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }
]

@app.route('/')
def index():
    """主页"""
    return render_template('index.html')

@app.route('/suppliers')
def suppliers():
    """供应商管理页面"""
    return render_template('suppliers.html', suppliers=SUPPLIERS)

@app.route('/suppliers/add', methods=['GET', 'POST'])
def add_supplier():
    """添加供应商"""
    if request.method == 'POST':
        new_supplier = {
            'id': len(SUPPLIERS) + 1,
            'name': request.form['name'],
            'contact': request.form['contact'],
            'phone': request.form['phone'],
            'address': request.form['address'],
            'products': request.form['products']
        }
        SUPPLIERS.append(new_supplier)
        flash('供应商添加成功！', 'success')
        return redirect(url_for('suppliers'))
    return render_template('add_supplier.html')

@app.route('/suppliers/edit/<int:supplier_id>', methods=['GET', 'POST'])
def edit_supplier(supplier_id):
    """编辑供应商"""
    supplier = next((s for s in SUPPLIERS if s['id'] == supplier_id), None)
    if not supplier:
        flash('供应商不存在！', 'error')
        return redirect(url_for('suppliers'))

    if request.method == 'POST':
        supplier.update({
            'name': request.form['name'],
            'contact': request.form['contact'],
            'phone': request.form['phone'],
            'address': request.form['address'],
            'products': request.form['products']
        })
        flash('供应商信息更新成功！', 'success')
        return redirect(url_for('suppliers'))
    return render_template('edit_supplier.html', supplier=supplier)

@app.route('/suppliers/delete/<int:supplier_id>')
def delete_supplier(supplier_id):
    """删除供应商"""
    global SUPPLIERS
    SUPPLIERS = [s for s in SUPPLIERS if s['id'] != supplier_id]
    flash('供应商删除成功！', 'success')
    return redirect(url_for('suppliers'))

@app.route('/logistics')
def logistics():
    """物流管理页面"""
    return render_template('logistics.html', logistics=LOGISTICS)

@app.route('/logistics/add', methods=['GET', 'POST'])
def add_logistics():
    """添加物流订单"""
    if request.method == 'POST':
        new_logistics = {
            'id': len(LOGISTICS) + 1,
            'order_id': request.form['order_id'],
            'supplier_id': int(request.form['supplier_id']),
            'destination': request.form['destination'],
            'status': '待出货',
            'created_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        LOGISTICS.append(new_logistics)
        flash('物流订单创建成功！', 'success')
        return redirect(url_for('logistics'))
    return render_template('add_logistics.html', suppliers=SUPPLIERS)

@app.route('/logistics/update_status/<int:logistics_id>', methods=['POST'])
def update_logistics_status(logistics_id):
    """更新物流状态"""
    logistics_item = next((l for l in LOGISTICS if l['id'] == logistics_id), None)
    if logistics_item:
        logistics_item['status'] = request.form['status']
        flash('物流状态更新成功！', 'success')
    else:
        flash('物流订单不存在！', 'error')
    return redirect(url_for('logistics'))

@app.route('/inventory')
def inventory():
    """库存管理页面"""
    return render_template('inventory.html', inventory=INVENTORY)

@app.route('/inventory/in/<int:item_id>', methods=['POST'])
def inventory_in(item_id):
    """商品入库"""
    item = next((i for i in INVENTORY if i['id'] == item_id), None)
    if item:
        quantity = int(request.form['quantity'])
        item['quantity'] += quantity
        flash(f'商品 {item["name"]} 入库 {quantity} 个，当前库存：{item["quantity"]}', 'success')
    else:
        flash('商品不存在！', 'error')
    return redirect(url_for('inventory'))

@app.route('/inventory/out/<int:item_id>', methods=['POST'])
def inventory_out(item_id):
    """商品出库"""
    item = next((i for i in INVENTORY if i['id'] == item_id), None)
    if item:
        quantity = int(request.form['quantity'])
        if item['quantity'] >= quantity:
            item['quantity'] -= quantity
            flash(f'商品 {item["name"]} 出库 {quantity} 个，当前库存：{item["quantity"]}', 'success')
        else:
            flash('库存不足！', 'error')
    else:
        flash('商品不存在！', 'error')
    return redirect(url_for('inventory'))

@app.route('/delivery')
def delivery():
    """配送管理页面"""
    return render_template('delivery.html', delivery=DELIVERY)

@app.route('/delivery/add', methods=['GET', 'POST'])
def add_delivery():
    """添加配送订单"""
    if request.method == 'POST':
        new_delivery = {
            'id': len(DELIVERY) + 1,
            'order_id': request.form['order_id'],
            'customer': request.form['customer'],
            'address': request.form['address'],
            'status': '准备中',
            'created_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        DELIVERY.append(new_delivery)
        flash('配送订单创建成功！', 'success')
        return redirect(url_for('delivery'))
    return render_template('add_delivery.html')

@app.route('/delivery/update_status/<int:delivery_id>', methods=['POST'])
def update_delivery_status(delivery_id):
    """更新配送状态"""
    delivery_item = next((d for d in DELIVERY if d['id'] == delivery_id), None)
    if delivery_item:
        delivery_item['status'] = request.form['status']
        flash('配送状态更新成功！', 'success')
    else:
        flash('配送订单不存在！', 'error')
    return redirect(url_for('delivery'))

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
