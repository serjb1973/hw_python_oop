class InfoMessage:
    """Информационное сообщение о тренировке."""

    def __init__(
            self,
            training_type: str,
            duration: float,
            distance: float,
            speed: float,
            calories: float):
        self.training_type = training_type
        self.duration = duration
        self.distance = distance
        self.speed = speed
        self.calories = calories

    def get_message(self):
        message = (
            f'Тип тренировки: {self.training_type}; '
            f'Длительность: {self.duration:.3f} ч.; '
            f'Дистанция: {self.distance:.3f} км; '
            f'Ср. скорость: {self.speed:.3f} км/ч; '
            f'Потрачено ккал: {self.calories:.3f}.')
        return message


class Training:
    """Базовый класс тренировки."""

    M_IN_KM: int = 1000
    LEN_STEP: float = 0.65

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
        distance = self.action * self.LEN_STEP / self.M_IN_KM
        return distance

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        speed = self.get_distance() / self.duration
        return speed

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        pass

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        info = InfoMessage(
            training_type=self.__class__.__name__,
            duration=self.duration,
            distance=self.get_distance(),
            speed=self.get_mean_speed(),
            calories=self.get_spent_calories())
        return info


class Running(Training):
    """Тренировка: бег."""

    LEN_STEP = 0.65

    def get_spent_calories(self) -> float:
        coeff_calorie_1 = 18
        coeff_calorie_2 = 20
        duration_min = self.duration * 60
        calories: float = ((
            coeff_calorie_1 * super().get_mean_speed() - coeff_calorie_2)
            * self.weight / self.M_IN_KM * duration_min)
        return calories


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""

    LEN_STEP = 0.65

    def __init__(
            self,
            action: int,
            duration: float,
            weight: float,
            height: float) -> None:
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:
        coeff_calorie_1 = 0.035
        coeff_calorie_2 = 0.029
        duration_min = self.duration * 60
        calories: float = ((
            coeff_calorie_1 * self.weight
            + (super().get_mean_speed()**2 // self.height) * coeff_calorie_2
            * self.weight) * duration_min)
        return calories


class Swimming(Training):
    """Тренировка: плавание."""

    LEN_STEP = 1.38

    def __init__(
            self, action: int,
            duration: float,
            weight: float,
            length_pool: int,
            count_pool: int) -> None:
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_mean_speed(self) -> float:
        speed: float = (
            self.length_pool * self.count_pool
            / self.M_IN_KM / self.duration)
        return speed

    def get_spent_calories(self) -> float:
        calories: float = (self.get_mean_speed() + 1.1) * 2 * self.weight
        return calories


def read_package(workout_type: str, data: list):
    """Прочитать данные полученные от датчиков."""
    training_dict = {
        'RUN': Running,
        'SWM': Swimming,
        'WLK': SportsWalking
    }
    class_run = training_dict[workout_type]
    training = class_run(*data)
    return training


def main(training: Training) -> None:
    """Главная функция."""
    info: InfoMessage = training.show_training_info()
    message = info.get_message()
    print(message)


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
