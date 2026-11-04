<template>
  <div class="p-5 h-full">
    <div class="flex justify-between mb-2">
      <span class="text-xl font-medium">{{ persianMonthNames[currentMonth - 1] }} {{ formatNumber(currentYear) }}</span>
      <div class="flex gap-x-1">
        <Button @click="decrementMonth" variant="ghost" class="h-4 w-4" icon="chevron-left" />
        <Button @click="incrementMonth" variant="ghost" class="h-4 w-4" icon="chevron-right" />
      </div>
    </div>

    <div class="h-[92%] min-h-[600px] min-w-[600px]">
      <div class="grid grid-cols-7 w-full pb-2">
        <span v-for="day in daysList" :key="day" class="text-center text-gray-600 font-normal text-sm">{{ day }}</span>
      </div>
      <div class="grid grid-cols-7 border-t-[1px] border-l-[1px] h-full w-full grid-rows-6">
        <div v-for="date in currentMonthDates" :key="date.toISOString()" class="border-r-[1px] border-b-[1px] border-gray-200">
          <div class="flex justify-center h-full font-normal mx-2" :class="currentMonthDate(date) ? 'text-gray-500' : 'text-gray-300'">
            <div v-if="currentMonthDate(date)" class="relative flex flex-col items-center w-full overflow-y-auto">
              <span class="py-1 sticky top-0 bg-white w-full text-center z-10" :class="isToday(date) && 'font-bold'">
                {{ formatPersianDay(date) }}
              </span>
              <div class="w-full">
                <CalendarEvent
                  v-for="calendarEvent in parsedData[parseDate(date)]"
                  :key="calendarEvent.name"
                  :event="calendarEvent"
                  :date="date"
                  class="mb-2 cursor-pointer w-full"
                  :draggable="false"
                />
              </div>
            </div>
            <span v-else>{{ formatPersianDay(date) }}</span>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed, ref } from 'vue'
import CalendarEvent from './CalendarEvent.vue'
import { Button } from 'frappe-ui'
import { groupBy } from '@/utils'

const props = defineProps({
  events: { type: Array, required: false, default: () => [] },
})

const persianMonthNames = [
  'فروردین', 'اردیبهشت', 'خرداد', 'تیر', 'مرداد', 'شهریور',
  'مهر', 'آبان', 'آذر', 'دی', 'بهمن', 'اسفند',
]
const daysList = ['شنبه', 'یکشنبه', 'دوشنبه', 'سه‌شنبه', 'چهارشنبه', 'پنجشنبه', 'جمعه']
const persianCalendar = new Intl.DateTimeFormat('en-US-u-ca-persian', {
  year: 'numeric',
  month: 'numeric',
  day: 'numeric',
})

function jalaliParts(date) {
  const parts = persianCalendar.formatToParts(date)
  return {
    year: Number(parts.find((part) => part.type === 'year').value),
    month: Number(parts.find((part) => part.type === 'month').value),
    day: Number(parts.find((part) => part.type === 'day').value),
  }
}

const todayParts = jalaliParts(new Date())
const currentMonth = ref(todayParts.month)
const currentYear = ref(todayParts.year)

const currentMonthDates = computed(() => {
  // Find the Gregorian date corresponding to the first day of this Jalali month.
  const approximate = new Date(currentYear.value + 621, currentMonth.value + 1, 15)
  let firstDay = null
  for (let offset = -25; offset <= 25; offset++) {
    const candidate = new Date(approximate)
    candidate.setDate(candidate.getDate() + offset)
    const parts = jalaliParts(candidate)
    if (parts.year === currentYear.value && parts.month === currentMonth.value && parts.day === 1) {
      firstDay = candidate
      break
    }
  }
  if (!firstDay) return []

  // Iranian weeks start on Saturday. JavaScript Sunday is day zero.
  const padding = (firstDay.getDay() + 1) % 7
  const gridStart = new Date(firstDay)
  gridStart.setDate(firstDay.getDate() - padding)
  return Array.from({ length: 42 }, (_, index) => {
    const date = new Date(gridStart)
    date.setDate(gridStart.getDate() + index)
    return date
  })
})

const parsedData = computed(() => groupBy(props.events || [], (row) => row.date))

function parseDate(date) {
  const dd = String(date.getDate()).padStart(2, '0')
  const mm = String(date.getMonth() + 1).padStart(2, '0')
  return `${date.getFullYear()}-${mm}-${dd}`
}

function formatNumber(value) {
  return new Intl.NumberFormat('fa-IR').format(value)
}

function formatPersianDay(date) {
  return new Intl.NumberFormat('fa-IR').format(jalaliParts(date).day)
}

function currentMonthDate(date) {
  const parts = jalaliParts(date)
  return parts.year === currentYear.value && parts.month === currentMonth.value
}

function isToday(date) {
  return date.toDateString() === new Date().toDateString()
}

function incrementMonth() {
  if (currentMonth.value === 12) {
    currentMonth.value = 1
    currentYear.value++
  } else {
    currentMonth.value++
  }
}

function decrementMonth() {
  if (currentMonth.value === 1) {
    currentMonth.value = 12
    currentYear.value--
  } else {
    currentMonth.value--
  }
}
</script>
