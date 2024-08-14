from fw.functions import Functions
import allure
import pytest


class TestCheckCostDelivery(Functions):
    # Совокупность граничных значений и классов эквивалентности
    changing_distance = [(1, 50), (2, 50), (3, 100), (5, 100), (9, 100), (10, 100), (11, 200), (16, 200), (29, 200), (30, 200), (31, 300), (47, 300)]

    @allure.title('Проверка изменения цены из-за расстояния')
    @pytest.mark.parametrize('distance, cost_only_for_distance', changing_distance)
    def test_check_cost_if_distance_is_changing(self, distance, cost_only_for_distance):
        # Подаем разные показатели расстояния
        if distance > 30:
            # Вводим данные по фиксированной стоимости доставки без учета расстояния (Габариты + хрупкость + загруженность)
            # и при этом вся стоимость не попадала под другие исключения (меньше 400р или расстояние больше 30 и хрупкости)
            cost_without_distance = 200
            result = self.shipping_cost_calculation(distance=distance, dimensions='большие', flag_fragility=False, service_load='Легкая')
        else:
            # Вводим данные по фиксированной стоимости доставки без учета расстояния (Габариты + хрупкость + загруженность)
            # и при этом не попадали под другие исключения (меньше 400р или расстояние больше 30 и хрупкости)
            cost_without_distance = 500
            result = self.shipping_cost_calculation(distance=distance, dimensions='большие', flag_fragility=True, service_load='Легкая')
        # Сравнение фактического результата с ожидаемым
        assert result - cost_without_distance == cost_only_for_distance

    changing_dimensions = [('большие', 200), ('маленькие', 100)]
    @allure.title('Проверка изменения цены из-за габаритов')
    @pytest.mark.parametrize('dimensions, cost_only_for_dimensions', changing_dimensions)
    def test_check_cost_if_dimensions_is_changing(self, dimensions, cost_only_for_dimensions):
        # Вводим данные по фиксированной стоимости доставки без учета габаритов (Расстояние + хрупкость + загруженность)
        # и при этом вся стоимость не попадала под другие исключения (меньше 400р или расстояние больше 30 и хрупкости)
        cost_without_dimensions = 500
        result = self.shipping_cost_calculation(distance=26, dimensions=dimensions, flag_fragility=True, service_load='Легкая')
        # Сравнение фактического результата с ожидаемым
        assert result - cost_without_dimensions == cost_only_for_dimensions

    changing_flag_fragility = [(True, 300), (False, 0)]
    @allure.title('Проверка изменения цены из-за хрупкости')
    @pytest.mark.parametrize('flag_fragility, cost_only_for_fragility', changing_flag_fragility)
    def test_check_cost_if_fragility_is_changing(self, flag_fragility, cost_only_for_fragility):
        # Вводим данные по фиксированной стоимости доставки без учета хрупкости (Расстояние + габариты + загруженность)
        # и при этом вся стоимость не попадала под другие исключения (меньше 400р или расстояние больше 30 и хрупкости)
        cost_without_fragility = 640
        result = self.shipping_cost_calculation(distance=26, dimensions='большие', flag_fragility=flag_fragility, service_load='Очень высокая')
        # Сравнение фактического результата с ожидаемым
        assert result - cost_without_fragility == cost_only_for_fragility*1.6  #Умножаю на 1.6, т.к. предполагаем, что загруженность в данных условиях = 1.6

    changing_service_load = [('очень высокая', 1.6), ('высокая', 1.4), ('повышенная', 1.2), ('легкая', 1)]
    @allure.title('Проверка изменения цены из-за загруженности службы доставки')
    @pytest.mark.parametrize('service_load, multiplication_factor', changing_service_load)
    def test_check_cost_if_service_load_is_changing(self, service_load, multiplication_factor):
        # Вводим данные по фиксированной стоимости доставки без учета загруженности (Расстояние + габариты + хрупкость)
        # и при этом вся стоимость не попадала под другие исключения (меньше 400р или расстояние больше 30 и хрупкости)
        cost_without_service_load = 700
        result = self.shipping_cost_calculation(distance=26, dimensions='большие', flag_fragility=True, service_load=service_load)
        # Сравнение фактического результата с ожидаемым
        assert result / cost_without_service_load == multiplication_factor

    # Тесты на исключение
    @allure.title('Проверка минимальной стоимости')
    def test_check_minimum_cost(self):
        # Подаем такие показатели, чтобы сумма доставки была меньше 400
        result = self.shipping_cost_calculation(distance=1, dimensions='маленькие', flag_fragility=False, service_load='Легкая')
        # Сравнение фактического результата с ожидаемым
        assert result == 400

    @allure.title('Проверка исключения хрупкости при расстояния более 30 км')
    def test_check_exception_fragility_if_distance_more_30_kilometers(self):
        # Подаем знак хрупкости и дистанцию больше 30 км
        result = self.shipping_cost_calculation(distance=43, dimensions='маленькие', flag_fragility=True, service_load='Легкая')
        # Сравнение фактического результата с ожидаемым
        assert result == 'Хрупкие грузы нельзя возить на расстояние более 30 км.'


    exception_for_not_correct_distance = [-3, 0]

    @allure.title('Проверка некорректных значений расстояния')
    @pytest.mark.parametrize('distance', exception_for_not_correct_distance)
    def test_check_not_correct_distance_value(self, distance):
        result = self.shipping_cost_calculation(distance=distance, dimensions='большие', flag_fragility=True, service_load='Легкая')
        # Сравнение фактического результата с ожидаемым
        assert result == 'Расстояние не может быть 0 или отрицательным.'

    @allure.title('Проверка некорректного значения габаритов')
    def test_check_not_correct_dimensions_value(self):
        result = self.shipping_cost_calculation(distance=5, dimensions='средние', flag_fragility=True, service_load='Легкая')
        # Сравнение фактического результата с ожидаемым
        assert result == 'Некорректное значение габаритов груза'