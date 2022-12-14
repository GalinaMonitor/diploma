from flask import Flask, session
from flask.globals import request
from flask_admin import Admin, expose, AdminIndexView
from flask_admin.contrib.sqla import ModelView
from flask_admin.contrib.sqla.form import InlineModelConverter
from flask_admin.model import InlineFormAdmin
from flask_admin.model.helpers import get_mdict_item_or_list
from flask_babelex import Babel
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import select

from backend.db.models import Sensor, SensorInfo

app = Flask(__name__)
babel = Babel(app)


@babel.localeselector
def get_locale():
	if request.args.get('lang'):
		session['lang'] = request.args.get('lang')
	return session.get('lang', 'ru')


app.config.from_prefixed_env()
db = SQLAlchemy()
db.init_app(app)


class DashBoardView(AdminIndexView):
	@expose('/')
	def add_data_db(self):
		sensors = db.session.scalars(
			select(Sensor)
		).all()
		return self.render('home.html', sensors=sensors)


# set optional bootswatch theme
app.config['FLASK_ADMIN_SWATCH'] = 'cerulean'

admin = Admin(
	app,
	index_view=DashBoardView(
		name='Домашняя страница',
		template='home.html',
		url='/'
	),
	name='Система управления удаленными сервисами умной теплицы',
	template_mode='bootstrap4',
)


class SensorInfoInlineAdmin(InlineFormAdmin):
	inline_converter = InlineModelConverter
	form_columns = ['id', 'datetime', 'data']
	column_labels = {
		'id': 'id',
		'datetime': 'Дата и время',
		'data': 'Данные'
	}


class SensorView(ModelView):
	form_columns = ['id', 'type', 'zone', 'sensor_info']
	column_searchable_list = ['id']
	column_filters = ['type', 'zone']
	form_choices = {
		'type': [(0, 'Влажность'), (1, 'Тепло')],
		'zone': [(0, 'Зона A'), (1, 'Зона B'), (2, 'Зона C'), (3, 'Зона D')]
	}
	column_choices = {
		'type': [(0, 'Влажность'), (1, 'Тепло')],
		'zone': [(0, 'Зона A'), (1, 'Зона B'), (2, 'Зона C'), (3, 'Зона D')]
	}
	column_labels = {
		'id': 'id',
		'type': 'Тип',
		'zone': 'Зона',
		'sensor_info': 'Данные',
	}
	inline_models = [SensorInfoInlineAdmin(SensorInfo)]
	edit_template = 'sensor.html'

	@expose('/edit/', methods=('GET', 'POST'))
	def edit_view(self):
		# Add sensor_info chart
		sensor_id = get_mdict_item_or_list(request.args, 'id')
		sensor = db.session.scalars(
			select(Sensor).where(Sensor.id == sensor_id)
		).one()
		sensor_info = [{'datetime': x.datetime.strftime("%y-%m-%d"), 'num': x.data} for x in sensor.sensor_info]
		self._template_args['sensor_info'] = sensor_info
		self._template_args['sensor'] = sensor
		res = super().edit_view()
		return res


admin.add_view(SensorView(Sensor, db.session, 'Датчики'))
