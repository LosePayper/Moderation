from enum import member

import disnake
import datetime

from disnake.ext import commands, tasks
from disnake.ext.commands import has_any_role

from database.UserInfoDatabase import UsersDataBase

user_db = UsersDataBase()
BANROLE = 1280239983818706974

class ModalDeleteWarn(disnake.ui.Modal):
    def __init__(self, member: disnake.Member):
        self.member = member

        components = [
            disnake.ui.TextInput(label="Причина предупреждения", placeholder="Введите причину снятия предупреждения",
                                 custom_id="reason")
        ]

        title = f"Снятие предупреждения у {member.name}"

        super().__init__(title=title, components=components, custom_id="modalDeleteWarn")

    async def callback(self, interaction: disnake.ModalInteraction) -> None:
        reason_Delete_Warn = interaction.text_values["reason"]

        await user_db.create_table_warns()
        result_check_db = await user_db.check_user_warndb(self.member.id)

        if result_check_db:  # Если пользователь есть в таблице тогда
            await user_db.delete_warn_user(self.member.id, 1)
            embed = disnake.Embed(color=disnake.Color.old_blurple(), title="Снятие предупреждения")
            embed.description = f"{interaction.author.mention}, вы успешно сняли предупреждение пользователю {self.member.mention} по причине {reason_Delete_Warn}"
            embed.set_thumbnail(url=interaction.author.display_avatar.url)
            await interaction.response.send_message(embed=embed, ephemeral=True)
        else:  # Если лож
            embed = disnake.Embed(color=disnake.Color.old_blurple(), title="Пользователя не найдено!")
            embed.description = f"{interaction.author.mention}, Пользователь {self.member.mention} " \
                                f"не найден в таблице."
            embed.set_thumbnail(url=interaction.author.display_avatar.url)
            await interaction.response.send_message(embed=embed, ephemeral=True)

class ModalDeleteRemark(disnake.ui.Modal):
    def __init__(self, member: disnake.Member):
        self.member = member

        components = [
            disnake.ui.TextInput(label="Причина отмены замечания", placeholder="Введите причину отмены замечания",
                                 custom_id="reason")
        ]

        title = f"Отмена замечания у {member.name}"

        super().__init__(title=title, components=components, custom_id="modalDeleteWarn")

    async def callback(self, interaction: disnake.ModalInteraction) -> None:
        reason_Delete_Warn = interaction.text_values["reason"]

        await user_db.create_table_warns()
        result_check_db = await user_db.check_user_warndb(self.member.id)

        if result_check_db:  # Если пользователь есть в таблице тогда
            await user_db.delete_remark_user(self.member.id, 1)
            embed = disnake.Embed(color=disnake.Color.old_blurple(), title="Отмена замечания")
            embed.description = f"{interaction.author.mention}, вы успешно отменили замечание у пользователя {self.member.mention} по причине {reason_Delete_Warn}"
            embed.set_thumbnail(url=interaction.author.display_avatar.url)
            await interaction.response.send_message(embed=embed, ephemeral=True)
        else:  # Если лож
            embed = disnake.Embed(color=disnake.Color.old_blurple(), title="Пользователя не найдено!")
            embed.description = f"{interaction.author.mention}, Пользователь {self.member.mention} " \
                                f"не найден в таблице."
            embed.set_thumbnail(url=interaction.author.display_avatar.url)
            await interaction.followup.send(embed=embed, ephemeral=True)

class ModalWarn(disnake.ui.Modal):
    def __init__(self, member: disnake.Member):
        self.member = member

        components = [
            disnake.ui.TextInput(label="Причина предупреждения", placeholder="Введите причину предупреждения",
                                 custom_id="reason")
        ]

        title = f"Выдача варна - {member.name}"

        super().__init__(title=title, components=components, custom_id="modalWarn")

    async def callback(self, interaction: disnake.ModalInteraction) -> None:
        reason = interaction.text_values["reason"]

        await user_db.create_table_warns()
        result_check_db = await user_db.check_user_warndb(self.member.id)

        if result_check_db:  # Если пользователь есть в таблице тогда
            if await user_db.get_user_warn_count(
                    self.member.id) >= 3:  # Проверяем количество предупреждений и кикаем если больше или равно 3
                await self.member.kick()
                await interaction.response.send_message(
                    "Количество предупреждений пользователя было больше 3-х он был изгнан с сервера.",
                    ephemeral=True)

            elif await user_db.get_user_warn_count(
                    self.member.id) < 3:  # Если меньше 3 тогда обновляем количество предупреждений
                await user_db.update_warns(interaction, self.member.id, 1)

                embed = disnake.Embed(color=disnake.Color.old_blurple(), title="Предупреждение выдано!")
                embed.description = f"{interaction.author.mention}, Вы успешно выдали предупреждение пользователю {self.member.mention}"
                embed.set_thumbnail(url=interaction.author.display_avatar.url)
                await interaction.response.send_message(embed=embed, ephemeral=True)

                if await user_db.get_user_warn_count(self.member.id) >= 3:  # Опять проверяем в случае истины кикаем
                    await self.member.kick()
                    await interaction.response.send_message(
                        "Количество предупреждений пользователя было больше 3-х он был изгнан с сервера.")
        else:  # Если лож
            await user_db.create_table_warns()
            await user_db.insert_warns(interaction, self.member.id, self.member.name, 1, 0, datetime.datetime.now())

            embed = disnake.Embed(color=disnake.Color.old_blurple(), title="Предупреждение выдано!")
            embed.description = f"{interaction.author.mention}, Вы успешно выдали предупреждение пользователю {self.member.mention}"
            embed.set_thumbnail(url=interaction.author.display_avatar.url)
            await interaction.response.send_message(embed=embed, ephemeral=True)

class ModalRemark(disnake.ui.Modal):
    def __init__(self, member: disnake.Member):
        self.member = member

        components = [
            disnake.ui.TextInput(label="Замечание", placeholder="Введите текст замечания",
                                 custom_id="reason")
        ]

        title = f"Замечание - {member.name}"

        super().__init__(title=title, components=components, custom_id="modalRemark")

    async def callback(self, interaction: disnake.ModalInteraction) -> None:
        reason = interaction.text_values["reason"]

        await user_db.create_table_warns()
        result_check_db = await user_db.check_user_warndb(self.member.id)

        if result_check_db:  # Если пользователь есть в таблице тогда
            if await user_db.get_user_remark_count(
                    self.member.id) >= 2:  # Проверяем количество замечаний и даем варн если больше или равно 2
                await user_db.update_warns(interaction, self.member.id, 1)
                await interaction.response.send_message(
                    "Количество замечаний пользователя было больше 2-х он был изгнан с сервера.",
                    ephemeral=True)

            elif await user_db.get_user_remark_count(
                    self.member.id) < 2:  # Если меньше 2 тогда обновляем количество предупреждений
                await user_db.update_remark(interaction, self.member.id, 1)

                embed = disnake.Embed(color=disnake.Color.old_blurple(), title="Замечание!")
                embed.description = f"{interaction.author.mention}, Вы успешно сделали замечание пользователю {self.member.mention}"
                embed.set_thumbnail(url=interaction.author.display_avatar.url)
                await interaction.response.send_message(embed=embed, ephemeral=True)

                if await user_db.get_user_remark_count(self.member.id) >= 2:  # Опять проверяем в случае истины варн
                    await user_db.update_warns(interaction, self.member.id, 1)
                    await interaction.followup.send(
                        "Количество замечаний пользователя было больше 2-х, ему было выдано предупреждение.")
                    await user_db.delete_remark_user(self.member.id, 2)
        else:  # Если лож
            await user_db.create_table_warns()
            await user_db.insert_warns(interaction, self.member.id, self.member.name, 0, 1)

            embed = disnake.Embed(color=disnake.Color.old_blurple(), title="Замечание!")
            embed.description = f"{interaction.author.mention}, Вы успешно сделали замечание пользователю {self.member.mention}"
            embed.set_thumbnail(url=interaction.author.display_avatar.url)
            await interaction.response.send_message(embed=embed, ephemeral=True)

class ModalBan(disnake.ui.Modal):
    def __init__(self, member: disnake.Member):
        self.member = member

        components = [
            disnake.ui.TextInput(label="Причина бана", placeholder="Введите причину бана", custom_id="reason")
        ]

        title = f"Забанить пользователя {member.name}"

        super().__init__(title=title, components=components, custom_id="modalBan")

    async def callback(self, interaction: disnake.ModalInteraction) -> None:
        reason = interaction.text_values["reason"]
        reason_text = str(reason)
        role = interaction.guild.get_role(BANROLE)
        embed = disnake.Embed(color=disnake.Color.old_blurple(), title=f"Мут пользователя - {self.member.name}")
        embed.description = f"{interaction.author.mention}, Вы успешно выдали бан пользователю {self.member.mention} по причине {reason_text}"
        embed.set_thumbnail(url=interaction.author.display_avatar.url)
        await interaction.response.send_message(embed=embed, ephemeral=False)
        await self.member.edit(roles=[])
        await self.member.add_roles(role)


class ModalMute(disnake.ui.Modal):
    def __init__(self, member: disnake.Member):
        self.member = member

        components = [
            disnake.ui.TextInput(label="Время мута (в минутах)", placeholder="Введите время мута",
                                 custom_id="time"),
            disnake.ui.TextInput(label="Причина мута", placeholder="Введите причину мута", custom_id="reason")
        ]
        title = f"Замутить пользователя {member.name}"
        super().__init__(title=title, components=components, custom_id="modalMute")
    async def callback(self, interaction: disnake.ModalInteraction) -> None:
        time_str = interaction.text_values["time"]
        reason = interaction.text_values["reason"]
        time_minutes = int(time_str)
        reason_text = str(reason)
        time = datetime.datetime.now() + datetime.timedelta(minutes=time_minutes)
        await self.member.timeout(until=time, reason=reason)
        embed = disnake.Embed(color=disnake.Color.old_blurple(), title=f"Мут пользователя - {self.member.name}")
        embed.description = f"{interaction.author.mention}, Вы успешно выдали мут пользователю {self.member.mention} на `{time_minutes}` минут по причине {reason_text}"
        embed.set_thumbnail(url=interaction.author.display_avatar.url)
        await interaction.response.send_message(embed=embed, ephemeral=False)


class ModalRename(disnake.ui.Modal):
    def __init__(self, member: disnake.Member):
        self.member = member

        components = [
            disnake.ui.TextInput(label="Новое имя пользователя", placeholder="Введите новое имя пользователя",
                                 custom_id="new_name"),
            disnake.ui.TextInput(label="Причина изменения", placeholder="Введите причину изменения", custom_id="reason")
        ]

        title = f"Изменение имени пользователя {member.name}"

        super().__init__(title=title, components=components, custom_id="modalRename")

    async def callback(self, interaction: disnake.ModalInteraction) -> None:
        new_name = interaction.text_values["new_name"]
        reason = interaction.text_values["reason"]

        await self.member.edit(nick=new_name)
        embed = disnake.Embed(color=disnake.Color.old_blurple(), title="Имя изменено!")
        embed.description = f"{interaction.author.mention}, Вы успешно изменили имя пользователю {self.member.mention} " \
                            f"на {new_name}"
        embed.set_thumbnail(url=interaction.author.display_avatar.url)
        await interaction.response.send_message(embed=embed, ephemeral=True)


class ButtonsAction(disnake.ui.View):
    def __init__(self, inter, member: disnake.Member):
        super().__init__(timeout=None)
        self.inter = inter
        self.member = member

    async def interaction_check(self, interaction):
        return interaction.user == self.inter.author

    async def ban_check(self, interaction: disnake.MessageInteraction) -> bool:
        ban_role_id = 1276614386932514949 # ID ролей для доступа к бану и разбану
        ban_role_id1 = 1276600091272155160
        ban_role_id2 = 1276600208284844052
        ban_role_id3 = 1276600240660807831
        return ban_role_id in [role.id for role in interaction.author.roles]
        return ban_role_id1 in [role.id for role in interaction.author.roles]

    async def mute_check(self, interaction: disnake.MessageInteraction) -> bool:
        mute_role_id = 1276606134924349562, 1276600275871862814, 1276606224225271909,  1276614386932514949, 1276600240660807831, 1276600091272155160, 1276600208284844052  # ID ролей для доступа к муту и размуту
        return mute_role_id in [role.id for role in interaction.author.roles]

    async def warn_check(self, interaction: disnake.MessageInteraction) -> bool:
        mute_role_id = 1276606134924349562, 1276600275871862814, 1276606224225271909,  1276614386932514949, 1276600240660807831, 1276600091272155160, 1276600208284844052  # ID ролей для доступа к муту и размуту
        return mute_role_id in [role.id for role in interaction.author.roles]

    async def unwarn_check(self, interaction: disnake.MessageInteraction) -> bool:
        mute_role_id = 1276600275871862814, 1276606224225271909,  1276614386932514949, 1276600240660807831, 1276600091272155160, 1276600208284844052  # ID ролей для доступа к муту и размуту
        return mute_role_id in [role.id for role in interaction.author.roles]

    async def remark_check(self, interaction: disnake.MessageInteraction) -> bool:
        mute_role_id = 1276606134924349562, 1276600275871862814, 1276606224225271909,  1276614386932514949, 1276600240660807831, 1276600091272155160, 1276600208284844052  # ID ролей для доступа к муту и размуту
        return mute_role_id in [role.id for role in interaction.author.roles]

    async def unremark_check(self, interaction: disnake.MessageInteraction) -> bool:
        mute_role_id = 1276600275871862814, 1276606224225271909,  1276614386932514949, 1276600240660807831, 1276600091272155160, 1276600208284844052  # ID ролей для доступа к муту и размуту
        return mute_role_id in [role.id for role in interaction.author.roles]

    async def rename_check(self, interaction: disnake.MessageInteraction) -> bool:
        ban_role_id = 1276614386932514949, 1276600091272155160, 1276600208284844052, 1276600240660807831  # ID ролей для доступа к бану и разбану
        return ban_role_id in [role.id for role in interaction.author.roles]

    @disnake.ui.button(label="Забанить", style=disnake.ButtonStyle.grey)
    async def ban(self, button: disnake.ui.Button, interaction: disnake.MessageInteraction):
        if await self.ban_check(interaction):
            if not self.member:
                await interaction.response.defer()
            else:
                await interaction.response.send_modal(ModalBan(self.member))
        else:
            await interaction.response.send_message("У вас недостаточно прав для выполнения этого действия.", ephemeral=True)

    @disnake.ui.button(label="Разбанить", style=disnake.ButtonStyle.grey)
    async def unban(self, button: disnake.ui.Button, interaction: disnake.MessageInteraction):
        role = interaction.guild.get_role(BANROLE)
        role_unverify = interaction.guild.get_role(1280934164681588746)
        if await self.ban_check(interaction):
            if not self.member:
                await self.member.remove_roles(role)
                await self.member.add_roles(role_unverify)
        else:
            await interaction.response.send_message("У вас недостаточно прав для выполнения этого действия.", ephemeral=True)

    @disnake.ui.button(label="Выдать мут", style=disnake.ButtonStyle.grey)
    async def mute(self, button: disnake.ui.Button, interaction: disnake.MessageInteraction):
        if await self.mute_check(interaction):
            if not self.member:
                await interaction.response.defer()
            else:
                await interaction.response.send_modal(ModalMute(self.member))
        else:
            await interaction.response.send_message("У вас недостаточно прав для выполнения этого действия.", ephemeral=True)

    @disnake.ui.button(label="Снять мут", style=disnake.ButtonStyle.grey)
    async def un_mute(self, button: disnake.ui.Button, interaction: disnake.MessageInteraction):
        if await self.mute_check(interaction):
            await self.member.timeout(until=None, reason=None)
        else:
            await interaction.response.send_message("У вас недостаточно прав для выполнения этого действия.", ephemeral=True)

    @disnake.ui.button(label="Выдать предупреждение", style=disnake.ButtonStyle.grey)
    async def warn(self, button: disnake.ui.Button, interaction: disnake.MessageInteraction):
        if await self.warn_check(interaction):
            if not self.member:
                await interaction.response.defer()
            else:
                await interaction.response.send_modal(ModalWarn(self.member))
        else:
            await interaction.response.send_message("У вас недостаточно прав для выполнения этого действия.", ephemeral=True)

    @disnake.ui.button(label="Снять предупреждение", style=disnake.ButtonStyle.grey)
    async def unwarn(self, button: disnake.ui.Button, interaction: disnake.MessageInteraction):
        if await self.unwarn_check(interaction):
            if not self.member:
                await interaction.response.defer()
            else:
                await interaction.response.send_modal(ModalDeleteWarn(self.member))
        else:
            await interaction.response.send_message("У вас недостаточно прав для выполнения этого действия.", ephemeral=True)

    @disnake.ui.button(label="Замечание", style=disnake.ButtonStyle.grey)
    async def remark(self, button: disnake.ui.Button, interaction: disnake.MessageInteraction):
        if await self.remark_check(interaction):
            if not self.member:
                await interaction.response.defer()
            else:
                await interaction.response.send_modal(ModalRemark(self.member))
        else:
            await interaction.response.send_message("У вас недостаточно прав для выполнения этого действия.", ephemeral=True)

    @disnake.ui.button(label="Отмена замечания", style=disnake.ButtonStyle.grey)
    async def unremark(self, button: disnake.ui.Button, interaction: disnake.MessageInteraction):
        if await self.unremark_check(interaction):
            if not self.member:
                await interaction.response.defer()
            else:
                await interaction.response.send_modal(ModalDeleteRemark(self.member))
        else:
            await interaction.response.send_message("У вас недостаточно прав для выполнения этого действия.", ephemeral=True)

    @disnake.ui.button(label="Изменить имя", style=disnake.ButtonStyle.grey)
    async def rename(self, button: disnake.ui.Button, interaction: disnake.MessageInteraction):
        if await self.rename_check(interaction):
            if not self.member:
                await interaction.response.defer()
            else:
                await interaction.response.send_modal(ModalRename(self.member))
        else:
            await interaction.response.send_message("У вас недостаточно прав для выполнения этого действия.", ephemeral=True)

    @disnake.ui.button(label="Отменить", style=disnake.ButtonStyle.red)
    async def delete(self, button: disnake.ui.Button, interaction: disnake.MessageInteraction):
        pass


class Action(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        print("[SYSTEM]: Модуль выдачи наказаний включен.")

    @commands.slash_command()
    @commands.has_any_role(1276606134924349562, 1276600275871862814, 1276606224225271909, 1276614386932514949, 1276600240660807831, 1276600091272155160, 1276600208284844052)
    async def action(self, inter, member: disnake.Member):
        """Взаимодействие с участником"""
        await user_db.create_table_warns()
        await user_db.check_user_warndb(member.id)
        countWarnsUser = await user_db.get_user_warn_count(member.id)
        countRemarkUser = await user_db.get_user_remark_count(member.id)
        embed = disnake.Embed(title=f"Взаимодействие с участником — {member.name}",
                              description=f"{inter.author.mention}, Выберите операцию для взаимодействия с {member.mention}",
                              colour=0x36393E)
        embed.add_field(name="**Присоединился:** ", value=disnake.utils.format_dt(member.joined_at, style="R"))
        embed.add_field(name="**Создан:** ", value=disnake.utils.format_dt(member.created_at, style="R"))
        embed.add_field(name="**Линк:** ", value=f"{member.mention}", inline=True)
        embed.add_field(name="**Статус:** ", value=f"`{member.status}`")
        embed.add_field(name="**Замечаний:** ", value=f"`{countRemarkUser}/2`")
        embed.add_field(name="**Предупреждений:** ", value=f"`{countWarnsUser}/3`", inline=True)
        embed.set_thumbnail(url=inter.author.avatar.url)
        await inter.send(embed=embed, view=ButtonsAction(inter, member))

    @commands.Cog.listener()
    async def on_button_click(self, inter):
        if inter.component.label == 'Отменить':
            await inter.message.delete()

def setup(bot: commands.Bot):
    bot.add_cog(Action(bot))
