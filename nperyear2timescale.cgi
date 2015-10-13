#!/bin/sh
if [ "$NPERYEAR" = 366 ]; then
  timescale="daily "
  month=day
elif [ "$NPERYEAR" = 365 ]; then
  timescale="daily "
  month=day
elif [ "$NPERYEAR" = 360 ]; then
  timescale="daily "
  month=day
elif [ "$NPERYEAR" = 73 ]; then
  timescale="pentad "
  month=pentad
elif [ "$NPERYEAR" = 36 ]; then
  timescale="decadal "
  month=decade
elif [ "$NPERYEAR" = 12 ]; then
  timescale="monthly "
  month=month
elif [ "$NPERYEAR" = 4 ]; then
  timescale="seasonal "
  month=season
elif [ "$NPERYEAR" = 1 ]; then
  timescale="annual "
  month=year
fi
