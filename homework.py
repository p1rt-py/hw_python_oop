

class InfoMessage:
    """Информационное сообщение о тренировке."""

    def __init__(self,
                 training_type: str,
                 duration: float,
                 distance: float,
                 speed: float,
                 calories: float
                 ) -> None:
        self.training_type = training_type
        self.duration = duration
        self.distance = distance
        self.speed = speed
        self.calories = calories

    def get_message(self) -> str:
        return (f'Тип тренировки: {self.training_type}; '
                f'Длительность: {self.duration:.3f} ч.; '
                f'Дистанция: {self.distance:.3f} км; '
                f'Ср. скорость: {self.speed:.3f} км/ч; '
                f'Потрачено ккал: {self.calories:.3f}.')


class Training:
    """Базовый класс тренировки."""
    LEN_STEP: float = 0.65
    M_IN_KM: float = 1000
    m_in_h: float = 60

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 ) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        # преодоленная_дистанция_за_тренировку / время_тренировки
        return self.get_distance() / self.duration

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        pass

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        message = InfoMessage(
                              self.__class__.__name__,
                              self.duration,
                              self.get_distance(),
                              self.get_mean_speed(),
                              self.get_spent_calories()
        )
        return message


class Running(Training):
    """Тренировка: бег."""
    cof_cal_1: float = 18
    cof_cal_2: float = 20

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float
                 ) -> None:
        super().__init__(action, duration, weight)
        # если убираю super, то не работает

    def get_spent_calories(self) -> float:
        cal_run2 = (self.duration * self.m_in_h)
        cal_run = (self.cof_cal_1 * self.get_mean_speed() - self.cof_cal_2)
        calories_run = cal_run * self.weight / self.M_IN_KM * cal_run2
        return calories_run


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    cof_cal_3: float = 0.035
    cof_cal_4: float = 0.029

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 height: float
                 ) -> None:
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:

        cal_wlk = ((self.get_mean_speed()**2) // self.height)
        cal_wlk2 = (self.duration * self.m_in_h)
        calories_walking = (self.cof_cal_3 * self.weight
                            + cal_wlk * self.cof_cal_4 * self.weight)\
            * cal_wlk2
        return calories_walking


class Swimming(Training):
    """Тренировка: плавание."""
    LEN_STEP: float = 1.38
    coeff_calorie_5: float = 1.1
    coeff_calorie_6: int = 2

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 length_pool: int,
                 count_pool: int
                 ) -> None:
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость при плавании."""
        swim_speed_1: float = self.length_pool * self.count_pool
        return swim_speed_1 / self.M_IN_KM / self.duration

    def get_spent_calories(self) -> float:
        swim_cal = self.get_mean_speed() + self.coeff_calorie_5
        calories_swim = swim_cal * self.coeff_calorie_6 * self.weight
        return calories_swim


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    training_dict = {
        'SWM': Swimming,
        'RUN': Running,
        'WLK': SportsWalking
    }
    # if workout_type in training_dict:
    #    return training_dict[workout_type](*data)
    # else:
    #    raise KeyError("Неизвестный тип тренировкт")
    # так мы избавляемся от елсе?
    if workout_type not in training_dict:
        raise KeyError
    return training_dict[workout_type](*data)


def main(training: Training) -> None:
    """Главная функция."""
    info: InfoMessage = training.show_training_info()
    print(info.get_message())


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
