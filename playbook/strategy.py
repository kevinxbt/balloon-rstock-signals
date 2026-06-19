"""
Balloon rStock Breakout Strategy
=================================
Volume-confirmed price breakout on Bitget rStock tokenized US equities.

Strategy Logic:
- Entry: price breaks above 20-bar high AND volume >= 2x 20-bar avg volume AND RSI 45-75
- Exit: stop loss -8%, take profit tier1 +15% (half), tier2 +30% (rest), time stop 14 bars
"""

from decimal import Decimal
from typing import Optional

from nautilus_trader.config import StrategyConfig
from nautilus_trader.model.data import Bar, BarType
from nautilus_trader.model.enums import OrderSide, TimeInForce
from nautilus_trader.model.identifiers import InstrumentId
from nautilus_trader.model.instruments import Instrument
from nautilus_trader.model.objects import Quantity
from nautilus_trader.trading.strategy import Strategy


class BalloonBreakoutConfig(StrategyConfig):
    instrument_id: Optional[InstrumentId] = None
    bar_type: Optional[BarType] = None
    instrument_ids: tuple[InstrumentId, ...] = ()
    bar_types: tuple[BarType, ...] = ()
    lookback_period: int = 20
    volume_multiplier: float = 2.0
    rsi_period: int = 14
    rsi_low: float = 45.0
    rsi_high: float = 75.0
    stop_loss_pct: float = 0.08
    tp1_pct: float = 0.15
    tp2_pct: float = 0.30
    time_stop_bars: int = 14
    trade_size: str = "10"


class BalloonBreakoutStrategy(Strategy):
    def __init__(self, config: BalloonBreakoutConfig) -> None:
        super().__init__(config)
        self.cfg = config
        self._closes: list[float] = []
        self._volumes: list[float] = []
        self._instrument: Optional[Instrument] = None
        self._entry_price: Optional[float] = None
        self._position: str = "NONE"
        self._bars_in_trade: int = 0
        self._tp1_hit: bool = False

    def on_start(self) -> None:
        bar_type = self.cfg.bar_type or (self.cfg.bar_types[0] if self.cfg.bar_types else None)
        instrument_id = self.cfg.instrument_id or (self.cfg.instrument_ids[0] if self.cfg.instrument_ids else None)
        if bar_type is None or instrument_id is None:
            raise RuntimeError("bar_type and instrument_id must be set")
        self._instrument = self.cache.instrument(instrument_id)
        self.subscribe_bars(bar_type)

    def on_bar(self, bar: Bar) -> None:
        close = float(bar.close)
        volume = float(bar.volume)
        self._closes.append(close)
        self._volumes.append(volume)
        if len(self._closes) < self.cfg.lookback_period + self.cfg.rsi_period + 5:
            return
        if self._position == "LONG":
            self._bars_in_trade += 1
        lookback = self.cfg.lookback_period
        prev_high = max(self._closes[-lookback - 1:-1])
        avg_volume = sum(self._volumes[-lookback - 1:-1]) / lookback
        rsi = self._compute_rsi(self._closes, self.cfg.rsi_period)
        instrument = self._instrument
        if instrument is None:
            return
        qty = Quantity(Decimal(self.cfg.trade_size), instrument.size_precision)
        if self._position == "LONG" and self._entry_price is not None:
            change_pct = (close - self._entry_price) / self._entry_price
            if change_pct <= -self.cfg.stop_loss_pct:
                self._close_all(instrument.id); self._reset(); return
            if not self._tp1_hit and change_pct >= self.cfg.tp1_pct:
                half_qty = Quantity(Decimal(self.cfg.trade_size) / 2, instrument.size_precision)
                self._submit(instrument.id, OrderSide.SELL, half_qty)
                self._tp1_hit = True
            if self._tp1_hit and change_pct >= self.cfg.tp2_pct:
                self._close_all(instrument.id); self._reset(); return
            if self._bars_in_trade >= self.cfg.time_stop_bars and change_pct < 0.05:
                self._close_all(instrument.id); self._reset(); return
        if self._position == "NONE":
            is_breakout = close > prev_high
            is_volume_confirmed = volume >= avg_volume * self.cfg.volume_multiplier
            is_rsi_ok = self.cfg.rsi_low <= rsi <= self.cfg.rsi_high
            if is_breakout and is_volume_confirmed and is_rsi_ok:
                self._submit(instrument.id, OrderSide.BUY, qty)
                self._entry_price = close
                self._position = "LONG"
                self._bars_in_trade = 0
                self._tp1_hit = False

    def _compute_rsi(self, closes: list[float], period: int) -> float:
        if len(closes) < period + 1:
            return 50.0
        deltas = [closes[i] - closes[i - 1] for i in range(-period, 0)]
        gains = [d for d in deltas if d > 0]
        losses = [-d for d in deltas if d < 0]
        avg_gain = sum(gains) / period if gains else 0.0
        avg_loss = sum(losses) / period if losses else 0.0
        if avg_loss == 0.0:
            return 100.0
        return 100.0 - (100.0 / (1.0 + avg_gain / avg_loss))

    def _submit(self, instrument_id, side, qty):
        order = self.order_factory.market(instrument_id=instrument_id, order_side=side, quantity=qty, time_in_force=TimeInForce.GTC)
        self.submit_order(order)

    def _close_all(self, instrument_id):
        for position in self.cache.positions_open(instrument_id=instrument_id):
            self._submit(instrument_id, OrderSide.SELL, position.quantity)

    def _reset(self):
        self._position = "NONE"; self._entry_price = None; self._bars_in_trade = 0; self._tp1_hit = False

    def on_stop(self):
        if self._instrument is not None:
            self.cancel_all_orders(self._instrument.id)
            self.close_all_positions(self._instrument.id)
