# Generated by Django 3.1.5 on 2021-03-25 04:40

from django.db import migrations, models
import django.db.models.deletion
import multiselectfield.db.fields


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0005_auto_20210325_1340'),
        ('papers', '0002_auto_20210215_1348'),
    ]

    operations = [
        migrations.AddField(
            model_name='verifyingexplanation',
            name='actual_legal_right_relationship',
            field=models.CharField(blank=True, max_length=248),
        ),
        migrations.AddField(
            model_name='verifyingexplanation',
            name='additional_info',
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name='verifyingexplanation',
            name='insurance',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='verifying_explanations', to='profiles.insurance'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='verifyingexplanation',
            name='lease_initiation_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='verifyingexplanation',
            name='mandatory_lease_period',
            field=models.PositiveSmallIntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='verifyingexplanation',
            name='rental_housing_registration_info',
            field=models.CharField(blank=True, max_length=35),
        ),
        migrations.AddField(
            model_name='verifyingexplanation',
            name='right_to_lease_contract_renewal',
            field=models.BooleanField(blank=True, default=None, null=True),
        ),
        migrations.AlterField(
            model_name='contractor',
            name='group',
            field=models.PositiveSmallIntegerField(choices=[(1, '임대인(매도인)'), (2, '임차인(매수인)'), (3, '공인중개사')]),
        ),
        migrations.AlterField(
            model_name='paper',
            name='options',
            field=multiselectfield.db.fields.MultiSelectField(blank=True, choices=[(1, '티비'), (2, '냉장고'), (3, '세탁기'), (4, '에어컨'), (5, '침대'), (6, '책상'), (7, '옷장'), (8, '신발장'), (9, '가스렌지'), (10, '전자렌지'), (11, '도어락'), (12, '비데'), (99, '추가물품')], max_length=29, null=True),
        ),
        migrations.AlterField(
            model_name='paper',
            name='trade_category',
            field=models.PositiveSmallIntegerField(choices=[(1, '월세'), (2, '전세'), (3, '매매'), (4, '교환')], default=1),
        ),
        migrations.AlterField(
            model_name='paperstatus',
            name='status',
            field=models.PositiveSmallIntegerField(choices=[(1, '요청중'), (2, '작성중'), (3, '서명중'), (4, '완료')], default=2),
        ),
        migrations.AlterField(
            model_name='verifyingexplanation',
            name='actual_building_category',
            field=models.PositiveSmallIntegerField(blank=True, choices=[(70, '제1종근린생활시설'), (71, '제2종근린생활시설'), (80, '단독주택'), (81, '아파트'), (99, '기타')], default=80),
        ),
        migrations.AlterField(
            model_name='verifyingexplanation',
            name='building_direction',
            field=models.CharField(max_length=15),
        ),
        migrations.AlterField(
            model_name='verifyingexplanation',
            name='building_other',
            field=models.CharField(blank=True, max_length=30),
        ),
        migrations.AlterField(
            model_name='verifyingexplanation',
            name='building_ownership',
            field=models.CharField(blank=True, max_length=30),
        ),
        migrations.AlterField(
            model_name='verifyingexplanation',
            name='building_structure',
            field=models.CharField(max_length=12),
        ),
        migrations.AlterField(
            model_name='verifyingexplanation',
            name='bus_stop',
            field=models.CharField(max_length=15),
        ),
        migrations.AlterField(
            model_name='verifyingexplanation',
            name='calculation_info',
            field=models.CharField(blank=True, max_length=200),
        ),
        migrations.AlterField(
            model_name='verifyingexplanation',
            name='department_store',
            field=models.CharField(max_length=15),
        ),
        migrations.AlterField(
            model_name='verifyingexplanation',
            name='drainage_status_info',
            field=models.CharField(blank=True, max_length=33),
        ),
        migrations.AlterField(
            model_name='verifyingexplanation',
            name='electricity_supply_status_info',
            field=models.CharField(blank=True, max_length=20),
        ),
        migrations.AlterField(
            model_name='verifyingexplanation',
            name='elementary_school',
            field=models.CharField(max_length=15),
        ),
        migrations.AlterField(
            model_name='verifyingexplanation',
            name='explanation_evidence_info',
            field=models.CharField(blank=True, max_length=15),
        ),
        migrations.AlterField(
            model_name='verifyingexplanation',
            name='explanation_evidences',
            field=multiselectfield.db.fields.MultiSelectField(choices=[(1, '등기권리증'), (2, '등기사항증명서'), (3, '토지대장'), (4, '건축물대장'), (5, '지적도'), (6, '임야도'), (7, '토지이용계획확인서'), (99, '기타')], max_length=16),
        ),
        migrations.AlterField(
            model_name='verifyingexplanation',
            name='gas_supply_status_info',
            field=models.CharField(blank=True, max_length=23),
        ),
        migrations.AlterField(
            model_name='verifyingexplanation',
            name='heating_status_info',
            field=models.CharField(blank=True, max_length=10),
        ),
        migrations.AlterField(
            model_name='verifyingexplanation',
            name='heating_supply_method',
            field=models.PositiveSmallIntegerField(choices=[(1, '중앙공급'), (2, '개별공급')]),
        ),
        migrations.AlterField(
            model_name='verifyingexplanation',
            name='heating_type',
            field=models.PositiveSmallIntegerField(choices=[(1, '도시가스'), (2, '기름'), (3, '프로판가스'), (4, '연탄'), (99, '그밖의종류')]),
        ),
        migrations.AlterField(
            model_name='verifyingexplanation',
            name='heating_type_info',
            field=models.CharField(blank=True, max_length=8),
        ),
        migrations.AlterField(
            model_name='verifyingexplanation',
            name='high_school',
            field=models.CharField(max_length=15),
        ),
        migrations.AlterField(
            model_name='verifyingexplanation',
            name='land_other',
            field=models.CharField(blank=True, max_length=30),
        ),
        migrations.AlterField(
            model_name='verifyingexplanation',
            name='land_ownership',
            field=models.CharField(blank=True, max_length=30),
        ),
        migrations.AlterField(
            model_name='verifyingexplanation',
            name='land_share',
            field=models.CharField(blank=True, max_length=12),
        ),
        migrations.AlterField(
            model_name='verifyingexplanation',
            name='ledger_building_category',
            field=models.PositiveSmallIntegerField(blank=True, choices=[(70, '제1종근린생활시설'), (71, '제2종근린생활시설'), (80, '단독주택'), (81, '아파트'), (99, '기타')], default=80),
        ),
        migrations.AlterField(
            model_name='verifyingexplanation',
            name='management',
            field=models.PositiveSmallIntegerField(choices=[(1, '위탁관리'), (2, '자체관리'), (99, '그 밖의 유형')]),
        ),
        migrations.AlterField(
            model_name='verifyingexplanation',
            name='matters_of_violation',
            field=models.CharField(blank=True, max_length=41),
        ),
        migrations.AlterField(
            model_name='verifyingexplanation',
            name='medical_center',
            field=models.CharField(max_length=15),
        ),
        migrations.AlterField(
            model_name='verifyingexplanation',
            name='middle_school',
            field=models.CharField(max_length=15),
        ),
        migrations.AlterField(
            model_name='verifyingexplanation',
            name='other_facilities',
            field=models.CharField(blank=True, max_length=69),
        ),
        migrations.AlterField(
            model_name='verifyingexplanation',
            name='other_use_restriction',
            field=models.CharField(blank=True, max_length=22),
        ),
        migrations.AlterField(
            model_name='verifyingexplanation',
            name='paper_categories',
            field=multiselectfield.db.fields.MultiSelectField(choices=[(1, '단독주택'), (2, '공동주택'), (3, '매매'), (4, '임대')], max_length=7),
        ),
        migrations.AlterField(
            model_name='verifyingexplanation',
            name='parking_lot',
            field=models.PositiveSmallIntegerField(choices=[(0, '없음'), (1, '전용주차시설'), (2, '공동주차시설'), (99, '그 밖의 주차시설')]),
        ),
        migrations.AlterField(
            model_name='verifyingexplanation',
            name='parking_lot_info',
            field=models.CharField(blank=True, max_length=10),
        ),
        migrations.AlterField(
            model_name='verifyingexplanation',
            name='payment_period',
            field=models.CharField(blank=True, max_length=200),
        ),
        migrations.AlterField(
            model_name='verifyingexplanation',
            name='planning_facilities',
            field=models.CharField(blank=True, max_length=50),
        ),
        migrations.AlterField(
            model_name='verifyingexplanation',
            name='relative_with_roads',
            field=models.CharField(max_length=26),
        ),
        migrations.AlterField(
            model_name='verifyingexplanation',
            name='rental_housing_registration',
            field=models.PositiveSmallIntegerField(choices=[(0, '해당사항없음'), (1, '장기일반민간임대주택'), (2, '공공지원민간임대주택'), (99, '그 밖의 유형')]),
        ),
        migrations.AlterField(
            model_name='verifyingexplanation',
            name='requesting_condition_info',
            field=models.CharField(blank=True, max_length=120),
        ),
        migrations.AlterField(
            model_name='verifyingexplanation',
            name='seismic_capacity',
            field=models.CharField(max_length=12),
        ),
        migrations.AlterField(
            model_name='verifyingexplanation',
            name='seismic_design',
            field=models.CharField(max_length=12),
        ),
        migrations.AlterField(
            model_name='verifyingexplanation',
            name='speculative_area',
            field=models.PositiveIntegerField(blank=True, choices=[(1, '토기투기지역'), (2, '주택투기지역'), (3, '투기과열지구')], null=True),
        ),
        migrations.AlterField(
            model_name='verifyingexplanation',
            name='subway_station',
            field=models.CharField(blank=True, max_length=15),
        ),
        migrations.AlterField(
            model_name='verifyingexplanation',
            name='undesirable_facilities_info',
            field=models.CharField(blank=True, max_length=20),
        ),
        migrations.AlterField(
            model_name='verifyingexplanation',
            name='unit_planning_area_others',
            field=models.CharField(blank=True, max_length=50),
        ),
        migrations.AlterField(
            model_name='verifyingexplanation',
            name='use_area',
            field=models.CharField(blank=True, max_length=21),
        ),
        migrations.AlterField(
            model_name='verifyingexplanation',
            name='use_district',
            field=models.CharField(blank=True, max_length=21),
        ),
        migrations.AlterField(
            model_name='verifyingexplanation',
            name='use_zone',
            field=models.CharField(blank=True, max_length=21),
        ),
        migrations.AlterField(
            model_name='verifyingexplanation',
            name='wall_crack_status_info',
            field=models.CharField(blank=True, max_length=28),
        ),
        migrations.AlterField(
            model_name='verifyingexplanation',
            name='wall_paper_status_info',
            field=models.CharField(blank=True, max_length=22),
        ),
        migrations.AlterField(
            model_name='verifyingexplanation',
            name='water_capacity_status_info',
            field=models.CharField(blank=True, max_length=25),
        ),
        migrations.AlterField(
            model_name='verifyingexplanation',
            name='water_damage_status_info',
            field=models.CharField(blank=True, max_length=25),
        ),
        migrations.AlterField(
            model_name='verifyingexplanation',
            name='water_leak_status_info',
            field=models.CharField(blank=True, max_length=28),
        ),
    ]
