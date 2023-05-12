import logging
import os.path
import ruamel.yaml
from datetime import date, timedelta, time
from order_parser import OrderParse

from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ContextTypes,
    filters,
    MessageHandler
)


default_cfg = """\
# place telegram bot token
tg_bot_token: ''

# daily order template
daily_order_template:
  enable: true  # true of false
  
  # notification time, using UTC
  # 24hr clock (1-24)
  notify_time: 8
"""

weekday_map_table: dict = {
    0: "Mon",
    1: "Tue",
    2: "Wed",
    3: "Thu",
    4: "Fri",
    5: "Sat",
    6: "Sun"
}

cfg: dict = {}

# noinspection SpellCheckingInspection
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)


def config_verify(config: dict):
    if config['tg_bot_token'] is None or config['tg_bot_token'] == "":
        logging.exception("tg_bot_token is empty!")
        exit()
    if config['daily_order_template']['enable'] is None:
        logging.exception("configuration error")
        exit()


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Hellow, this is BlissfulAlloy79's Bot!"
    )


async def order(update: Update, context: ContextTypes.DEFAULT_TYPE):
    order_raw = update.message.text.replace("/order ", '')
    logging.info(order_raw)
    try:
        interp = OrderParse(order_raw)

        t_order = interp.get_total()
        f_order = interp.get_food()
        d_order = interp.get_drinks()
        logging.info(f"Total orders: {t_order}")
        logging.info(f"Food orders: {f_order}")
        logging.info(f"Drink orders: {d_order}")

        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=f"Received order:\n{order_raw}"
        )

        order_date = interp.get_date()
        # send order msg
        formatted_text = f"{order_date}\n"
        formatted_text += "華仁\n\n"
        formatted_text += f"Total: $38x{t_order} = ${38 * t_order}\n\n"
        for i in f_order.keys():
            formatted_text += f"{i} x{f_order[i]}\n"
        formatted_text += "\n"
        for i in d_order.keys():
            formatted_text += f"{i} x{d_order[i]}\n"
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=formatted_text
        )

        # generate checklist in Markdown format
        check_text = f"{order_date}\n\n"
        check_text += f"Total: $38x{t_order} = ${38 * t_order}\n\n"
        for i in interp.order:
            check_text += f"[ ] {i}\n\n"
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=check_text
        )

    except SyntaxError as e:
        logging.error(e)
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=f"An error occurred: {e}"
        )


async def daily_order_template(context: ContextTypes.DEFAULT_TYPE):
    msg_date = date.today() + timedelta(days=1)
    order_template: str = f"{msg_date} {weekday_map_table[date.weekday(msg_date)]}"
    order_template += "\n\n\n\n"
    order_template += "Copy this message and add here\n"
    order_template += "👀Menu in group media\n"
    order_template += "You MUST pay your money (e-payment or cash) before lunchtime"
    await context.bot.send_message(
        chat_id='1962207202',
        text=order_template
    )


async def get_chat_id(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=update.effective_chat.id
    )


async def unknown(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Unknown command, please check your input"
    )


if __name__ == '__main__':
    yaml = ruamel.yaml.YAML()

    if not os.path.exists('config.yml'):
        yaml_str = yaml.load(default_cfg)
        with open('config.yml', 'w', encoding='utf-8') as y:
            yaml.dump(yaml_str, y)
        logging.exception("Config file not set up yet!")
        exit()

    with open(r'config.yml', encoding='utf-8') as f:
        cfg = yaml.load(f)
        config_verify(cfg)

    application = ApplicationBuilder().token(cfg['tg_bot_token']).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("order", order))
    application.add_handler(CommandHandler("id", get_chat_id))
    application.add_handler(MessageHandler(filters.COMMAND, unknown))

    if cfg['daily_order_template']['enable'] is True:
        application.job_queue.run_daily(daily_order_template,
                                        time=time(hour=cfg['daily_order_template']['notify_time']),
                                        days=(0, 1, 2, 3, 4))

    application.run_polling()
