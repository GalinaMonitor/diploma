from flask import Flask, session
from flask.globals import request
from flask_admin import Admin, expose, AdminIndexView
from flask_admin.contrib.sqla import ModelView
from flask_admin.model.helpers import get_mdict_item_or_list
from flask_babelex import Babel
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import select

from backend.db.models import Sensor, Device

app = Flask(__name__)
babel = Babel(app)


@babel.localeselector
def get_locale():
	if request.args.get('lang'):
		session['lang'] = request.args.get('lang')
	return session.get('lang', 'ru')


app.config.from_prefixed_env()
db = SQLAlchemy(session_options={"autoflush": False})
db.init_app(app)

type_dict = {
	0: 'Влажность',
	1: 'Тепло'
}

zone_dict = {
	0: 'Зона A',
	1: 'Зона B',
	2: 'Зона C',
	3: 'Зона D'
}

operating_mode_dict = {
	0: 'LOW',
	1: 'MEDIUM',
	2: 'HIGH',
}


class DashBoardView(AdminIndexView):
	@expose('/')
	def add_data_db(self):
		sensors = db.session.scalars(
			select(Sensor)
		).all()
		for sensor in sensors:
			sensor.type = type_dict[sensor.type]
			sensor.zone = zone_dict[sensor.zone]
			for sensor_data in sensor.sensor_info:
				sensor_data.datetime = sensor_data.datetime.strftime("%Y-%m-%d %H:%M")
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


class SensorView(ModelView):
	form_columns = ['id', 'name', 'type', 'zone', 'max_value']
	list_columns = ['id', 'name', 'type', 'zone', 'max_value']
	column_searchable_list = ['id']
	column_filters = ['type', 'zone']
	form_choices = {
		'type': type_dict.items(),
		'zone': zone_dict.items()
	}
	column_choices = {
		'type': type_dict.items(),
		'zone': zone_dict.items()
	}
	column_labels = {
		'id': 'id',
		'name': 'Название',
		'type': 'Тип',
		'zone': 'Зона',
		'max_value': 'Максимальное значение'
	}
	edit_template = 'sensor.html'

	@expose('/edit/', methods=('GET', 'POST'))
	def edit_view(self):
		# Add sensor_info chart
		sensor_id = get_mdict_item_or_list(request.args, 'id')
		sensor = db.session.scalars(
			select(Sensor).where(Sensor.id == sensor_id)
		).one()
		sensor_info = [{'datetime': x.datetime.strftime("%y-%m-%d"), 'num': x.data} for x in sensor.sensor_info]
		max_value = max(sensor_info, key=lambda x: x['num'])['num']
		self._template_args['sensor_info'] = sensor_info
		self._template_args['sensor'] = sensor

		self._template_args['warning'] = max_value > sensor.max_value
		res = super().edit_view()
		return res


class DeviceView(ModelView):
	form_columns = ['id', 'name', 'is_active', 'operating_mode', 'zone', 'sensor_id', 'sensor']
	list_columns = ['id', 'name', 'is_active', 'operating_mode', 'zone', 'sensor_id', 'sensor']
	column_searchable_list = ['id']
	column_filters = ['zone']
	form_choices = {
		'operating_mode': operating_mode_dict.items(),
		'zone': zone_dict.items()
	}
	column_choices = {
		'zone': zone_dict.items(),
		'operating_mode': operating_mode_dict.items(),
	}
	column_labels = {
		'id': 'id',
		'name': 'Название',
		'sensor': 'Связанный датчик',
		'is_active': 'Активен',
		'zone': 'Зона',
		'operating_mode': 'Режим работы',
		'sensor_id': 'ID связанного датчика'
	}


admin.add_view(SensorView(Sensor, db.session, 'Датчики'))
admin.add_view(DeviceView(Device, db.session, 'Устройства'))
