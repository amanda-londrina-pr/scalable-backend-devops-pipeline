import random

from faker import Faker

from app.domain.enums.task_status import TaskStatus

fake = Faker("pt_BR")


def generate_task_data():
    status = random.choice(
        [
            TaskStatus.PENDING,
            TaskStatus.IN_PROGRESS,
            TaskStatus.DONE,
        ]
    )

    title = fake.sentence(nb_words=4)

    if status == TaskStatus.DONE:
        description = f"[FINALIZADO] {fake.paragraph()}"
    elif status == TaskStatus.IN_PROGRESS:
        description = f"[EM ANDAMENTO] {fake.paragraph()}"
    else:
        description = fake.paragraph()

    return {
        "title": title,
        "description": description,
        "status": status,
    }
