import mysql.connector
import json
import random
import os
from datetime import datetime, timedelta


db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': '***',
    'database': 'support_call_centre_database',
}

json_dir =  './telephony_api_mocks'

os.makedirs(json_dir, exist_ok=True)

def generate_data():
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()
    teams = ['First Line Support', 'Second Line Support', 'Third Line Support']
    names = [
        'Adele Buckley', 'Adeline Ware', 'Adelynn Neal', 'Ahmad Long', 'Alayah Morrow',
        'Alden Huber', 'Alena Lara', 'Alina Dean', 'Amaia Ho', 'Amora Zhang',
        'Amoura Peck', 'Anders Preston', 'Angel Carlson', 'Angelo Daniel', 'Angelo McMillan',
        'Annabelle Heath', 'Arabella Cisneros', 'Arian Velasquez', 'Arthur Shepherd', 'Aryan McMahon',
        'Axton Wise', 'Bear Ventura', 'Beckham Solis', 'Beckett Mosley', 'Belen Gentry',
        'Blakely Espinosa', 'Bowen King', 'Braelyn Jacobs', 'Brayden Powell', 'Braylee Franco',
        'Brennan Weber', 'Briana Everett', 'Briar Knox', 'Bridget Mendoza', 'Briggs Beck',
        'Bryan Berger', 'Bryan Riley', 'Bryant Hammond', 'Bryant Hendrix', 'Caiden Wall',
        'Camilo McDonald', 'Camille Alexander', 'Carmelo Bravo', 'Castiel Phelps', 'Catherine Vaughan',
        'Chandler McMahon', 'Charlotte Wu', 'Cheyenne Beltran', 'Clare Aguilar', 'Cleo Kelley',
        'Cohen Schaefer', 'Collins Quintero', 'Cristian Sheppard', 'Daisy Choi', 'Daniella Estes',
        'Danna Greer', 'Davian Taylor', 'Deandre Benson', 'Dennis Mosley', 'Dominic Nielsen',
        'Dorian Beasley', 'Eleanor Sullivan', 'Eliza Knight', 'Elliana Chen', 'Emmanuel Romero',
        'Ephraim Stafford', 'Eric Silva', 'Esteban Leon', 'Evan Simon', 'Ezekiel Morse',
        'Forrest Gross', 'Gabrielle Harrington', 'Gael Oliver', 'Gage Hicks', 'Garrett Glass',
        'Gemma Bauer', 'Genevieve Stevens', 'Gia Horton', 'Gordon Hood', 'Gwen Good',
        'Hadlee Combs', 'Hadleigh Allison', 'Hakeem Wyatt', 'Harold Espinosa', 'Harvey Jimenez',
        'Holly Barajas', 'Indie Rasmussen', 'Isabella Winters', 'Isaias Watts', 'Isaiah McKenzie',
        'Isaiah Williamson', 'Ivy Jacobs', 'Iyla Parrish', 'Jade Mendez', 'Jaime Raymond',
        'Jakob Howell', 'Janiyah Gonzales', 'Jayda Jackson', 'Jaylah Fisher', 'Jayleen Francis',
        'Jenna Crosby', 'Jerry Li', 'Jessica Weeks', 'Jimmy Edwards', 'Jocelyn McClain',
        'Johan Solis', 'Jonah Bond', 'Jordan Porter', 'Joy Melendez', 'Judson Dixon',
        'Junior Drake', 'Justin Santiago', 'Kaia Bowers', 'Kairi Pierce', 'Kalani Ayers',
        'Kaliyah Levy', 'Kane Hughes', 'Karsyn Charles', 'Karsyn Lee', 'Karter Richardson',
        'Katalina Orozco', 'Kayla Barrett', 'Keanu Deleon', 'Khari York', 'Khalid Stevenson',
        'Kieran Proctor', 'Kingston Santana', 'Knox Ross', 'Koda Hess', 'Kora Santiago',
        'Kyree Casey', 'Kyree Price', 'Kyson Barton', 'Laney Bryant', 'Lauren English',
        'Laylah Sanford', 'Leilani Yoder', 'Leland Acosta', 'Leonardo Hart', 'Leyla Morrow',
        'Liberty Chapman', 'Lilianna Watkins', 'Lionel Potter', 'Lucia Snyder', 'Macie Yu',
        'Madisyn Austin', 'Magnus Berry', 'Makenna Gomez', 'Malik Perez', 'Marcellus Gilbert',
        'Marcus Walls', 'Mavis Rubio', 'Maxine Archer', 'Mckenna Travis', 'Melissa Russo',
        'Milan Munoz', 'Milan Pena', 'Miley Wang', 'Milo Wilkerson', 'Mira Koch',
        'Miracle Hubbard', 'Miracle Pugh', 'Miracle Trevino', 'Mitchell Reed', 'Morgan Vang',
        'Muhammad Eaton', 'Myra Johnson', 'Nash Case', 'Nasir Cuevas', 'Nicolas Warner',
        'Nikolas Short', 'Noah Holt', 'Nyla Harris', 'Oakleigh Barrett', 'Omari Dudley',
        'Omar Henry', 'Paige Jaramillo', 'Paul McIntosh', 'Peyton Estrada', 'Phoenix Solis',
        'Piper Byrd', 'Raquel Miranda', 'Regina Deleon', 'Ricky Nielsen', 'Riggs Meyers',
        'Robert Medina', 'Ronan Logan', 'Rory Brooks', 'Rory Delarosa', 'Ryleigh Fuentes',
        'Salvador Lamb', 'Samantha Yu', 'Samuel Hardy', 'Sariah Copeland', 'Scarlett Parrish',
        'Scarlette Curry', 'Sebastian Vance', 'Sofia Thornton', 'Stetson Alvarez', 'Summer Gomez',
        'Sylas Ali', 'Sylvia Guerra', 'Tadeo Grimes', 'Thatcher McCormick', 'Thiago Hickman',
        'Titan House', 'Tristen Brown', 'Truett Pierce', 'Ulises Miller', 'Valentin Burke',
        'Valentina Wilkerson', 'Vera Cook', 'Victoria Mack', 'Vienna Houston', 'Vienna Vo',
        'Vivian Bennett', 'Will Lin', 'Willie Hunt', 'Wren Greer', 'Wynter Vang',
        'Yousef Moses', 'Zachary Lawrence', 'Zaniyah Clarke', 'Zaniyah Rivers', 'Zelda Wilcox',
        'Zhuri Blackwell', 'Zora Curtis'
    ]
    employees_inf = []
    for i in range (1, 51):
        full_name = random.choice(names)
        team = random.choice(teams)
        hire_date = datetime.now().date() - timedelta(days = random.randint(10, 1000))
        employees_inf.append((i, full_name, team, hire_date))

    cursor.executemany("INSERT IGNORE INTO employees (employee_id, full_name, team, hire_date) VALUES (%s, %s, %s, %s)", employees_inf)

    for call_id in range(40):
        employee_id = random.randint(1, 50)
        call_time = datetime.now() - timedelta(minutes = random.randint(1, 300))
        phone = f"+380{random.randint(100000000,999999999)}"
        direction = random.choice(['inbound', 'outbound'])
        status = 'completed'

        cursor.execute(
            "INSERT IGNORE INTO calls (call_id, employee_id, call_time, phone, direction, status) VALUES (%s, %s, %s, %s, %s, %s)",
            (call_id, employee_id, call_time, phone, direction, status)
        )

        telephony_data = {
            'call_id': call_id,
            'duration_sec': random.randint(10, 1000),
            'short_description': random.choice([
                "Customer asked about billing issues",
                "Technical problem with login resolved",
                "Inquiry about new subscription plans",
                "Call dropped due to network issues",
                "User reported unable to access the mobile app after the latest update.",
                "Customer needs help resetting their two-factor authentication (2FA).",
                "Technical issue with slow dashboard loading speeds; ticket escalated.",
                "Password reset successful; user guided through the security settings.",
                "Bug report: User cannot export PDF reports on the MacOS version.",
                "Poor audio quality on customer side; most of the conversation was inaudible.",
                "Positive feedback: User very satisfied with the quick resolution.",
                "Wrong department reached; agent successfully redirected the call.",
                "User requested a callback from a senior manager regarding account terms.",
                "Customer asked to cancel subscription; retention offer was declined.",
                "Long wait time complaint; customer was frustrated but issue resolved."
            ])
        }

        with open(f"{json_dir}/call_{call_id}.json", "w") as file:
            json.dump(telephony_data, file)

    conn.commit()
    cursor.close()
    conn.close()


generate_data()
