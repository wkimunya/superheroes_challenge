from random import random, choice as rc
from app import app
from models import db, Hero, Power, HeroPower


power_list = [
  { "name": "super strength", "description": "gives the wielder super-human strengths" },
  { "name": "flight", "description": "gives the wielder the ability to fly through the skies at supersonic speed" },
  { "name": "super human senses", "description": "allows the wielder to use her senses at a super-human level" },
  { "name": "elasticity", "description": "can stretch the human body to extreme lengths" }
]


hero_list = [
  { "name": "Kamala Khan", "super_name": "Ms. Marvel" },
  { "name": "Doreen Green", "super_name": "Squirrel Girl" },
  { "name": "Gwen Stacy", "super_name": "Spider-Gwen" },
  { "name": "Janet Van Dyne", "super_name": "The Wasp" },
  { "name": "Wanda Maximoff", "super_name": "Scarlet Witch" },
  { "name": "Carol Danvers", "super_name": "Captain Marvel" },
  { "name": "Jean Grey", "super_name": "Dark Phoenix" },
  { "name": "Ororo Munroe", "super_name": "Storm" },
  { "name": "Kitty Pryde", "super_name": "Shadowcat" },
  { "name": "Elektra Natchios", "super_name": "Elektra" }
]

strengths = ["Strong", "Weak", "Average"]

with app.app_context():

  Hero.query.delete()
  Power.query.delete()
  HeroPower.query.delete()

  print("🦸‍♀️ Seeding heroes...")
  heroes = []
  for hero in hero_list:
    hr = Hero(
      name = hero["name"],
      super_name = hero["super_name"]
    )
    heroes.append(hr)
  db.session.add_all(heroes)
  db.session.commit()

  print("🦸‍♀️ Seeding powers...")
  powers = []
  for power in power_list:
    pw = Power(
      name = power["name"],
      description = power["description"]
    )
    powers.append(pw)
  db.session.add_all(powers)
  db.session.commit()

  print("🦸‍♀️ Adding powers to heroes...")
  hero_powers = []
  for hero in heroes:
    hero_power = HeroPower(
      hero = rc(heroes),
      power = rc(powers),
      strength = rc(strengths)
    )
    hero_powers.append(hero_power)
  db.session.add_all(hero_powers)
  db.session.commit()

  print("🦸‍♀️ Done seeding!")
