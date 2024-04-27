async def on_member_join(member):
  if "join_role" in db:
    role_id = db["join_role"]
    role = member.guild.get_role(role_id)
    if role:
      await member.add_roles(role)
      print(f"Added role {role.name} to {member.name}")
  if "welcome_message_enabled" in db and db["welcome_message_enabled"]:
    if "welcome_message" in db:
      welcome_message = db["welcome_message"]
      await member.send(welcome_message)
      print(f"Sent welcome message to {member.name}")
    