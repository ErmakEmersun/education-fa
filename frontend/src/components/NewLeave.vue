<template lang="">
  <div class="flex flex-col gap-4">
    <div v-for="section in allFields" :key="section.section">
      <div class="grid grid-cols-1 gap-4">
        <div
          v-for="field in section.fields"
          :key="field.name"
          :class="field.hidden && 'hidden'"
        >
          <div class="mb-2 text-sm text-gray-600">{{ field.label }}</div>
          <FormControl
            v-if="field.type === 'select'"
            type="select"
            :options="field.options"
            v-model="newLeave[field.name]"
            :default="field.default"
            @change="(e) => field.change(e.target.value)"
          />
          <div v-else-if="field.type === 'date'">
            <FormControl
              type="date"
              v-model="newLeave[field.name]"
              @change="(e) => field.change(e.target.value)"
            />
            <ErrorMessage
              v-if="isBeforeError && field.name === 'from_date'"
              :message="errorMessage"
              class="pt-2"
            />
            <ErrorMessage
              v-if="isAfterError && field.name === 'to_date'"
              :message="errorMessage"
              class="pt-2"
            />
          </div>
          <FormControl
            v-else
            :type="field.type"
            v-model="newLeave[field.name]"
            :placeholder="field.placeholder"
            :disabled="field.readonly"
          />
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { FormControl, ErrorMessage } from 'frappe-ui'
import dayjs from 'dayjs'
import { ref } from 'vue'

const props = defineProps({
  newLeave: {
    type: Object,
    required: true,
  },
})
const { newLeave } = props

const isAfterError = ref(false)
const isBeforeError = ref(false)
const errorMessage = ref('')

function getDateDiff(from_date, to_date) {
  to_date = dayjs(newLeave.to_date)
  from_date = dayjs(newLeave.from_date)
  return to_date.diff(from_date, 'd') || 0
}

function setErrorMessage(diff = 0, dateType) {
  if (diff < 0) {
    if (dateType === 'from_date') {
      isBeforeError.value = true
      errorMessage.value = 'تاریخ شروع باید پیش از تاریخ پایان باشد'
      newLeave.total_days = 0
    } else if (dateType === 'to_date') {
      isAfterError.value = true
      errorMessage.value = 'تاریخ پایان باید پس از تاریخ شروع باشد'
      newLeave.total_days = 0
    }
  } else {
    isBeforeError.value = false
    isAfterError.value = false
    newLeave.total_days = diff + 1
  }
}

const allFields = [
  {
    section: 'اطلاعات مرخصی',
    fields: [
      {
        label: 'فراگیر',
        name: 'student',
        type: 'data',
        readonly: true,
      },
    ],
  },
  {
    section: 'اطلاعات تاریخ',
    fields: [
      {
        label: 'از تاریخ',
        name: 'from_date',
        type: 'date',
        change: (value) => {
          let date_diff = getDateDiff(newLeave.from_date, newLeave.to_date)
          setErrorMessage(date_diff, 'from_date')
        },
      },
      {
        label: 'تا تاریخ',
        name: 'to_date',
        type: 'date',
        change: (value) => {
          let date_diff = getDateDiff(newLeave.from_date, newLeave.to_date)
          setErrorMessage(date_diff, 'to_date')
        },
      },
      {
        label: 'تعداد روزها',
        name: 'total_days',
        type: 'number',
        readonly: true,
      },
      {
        label: 'دلیل',
        name: 'reason',
        type: 'textarea',
      },
    ],
  },
]
</script>
