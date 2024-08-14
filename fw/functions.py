import allure

class Functions():

    @allure.step('Расчет стоимости доставки')
    def shipping_cost_calculation(self, distance, dimensions, flag_fragility, service_load):
        cost = 0

        # Расстояние
        distance = int(distance)
        if 0 < distance <= 2:
            cost += 50
        elif 2 < distance <= 10:
            cost += 100
        elif 10 < distance <= 30:
            cost += 200
        elif distance > 30:
            cost += 300
        else:
            return 'Расстояние не может быть 0 или отрицательным.'

        # Габариты
        if dimensions.lower() == 'большие':
            cost += 200
        elif dimensions.lower() == 'маленькие':
            cost += 100
        else:
            return 'Некорректное значение габаритов груза'

        # Хрупкость груза
        if flag_fragility:
            if distance <= 30:
                cost += 300
            # Исключение для хрупкости и расстояния
            else:
                return 'Хрупкие грузы нельзя возить на расстояние более 30 км.'

        # Загруженность службы доставки
        if service_load.lower() == 'очень высокая':
            cost *= 1.6
        elif service_load.lower() == 'высокая':
            cost *= 1.4
        elif service_load.lower() == 'повышенная':
            cost *= 1.2

        # Исключение на минимальную сумму доставки
        if cost < 400:
            cost = 400

        return cost
