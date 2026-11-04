<template>
  <div>
    <div class="flex flex-col gap-4">
      <div v-for="section in allFields" :key="section.section">
        <div class="grid grid-cols-3 gap-4">
          <div
            v-for="field in section.fields"
            :key="field.name"
            :class="field.hidden && 'hidden'"
          >
            <div class="mb-2 text-sm text-gray-600">{{ field.label }}</div>
            <FormControl
              :type="field.type"
              v-model="updatedStudentProfile[field.name]"
              :placeholder="field.label"
              :disabled="field.readonly"
            />
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { FormControl, ErrorMessage } from 'frappe-ui'
import { onMounted, reactive, ref, computed, watch } from 'vue'

const props = defineProps({
  updatedStudentProfile: {
    type: Object,
    required: true,
  },
  editMode: {
    type: Boolean,
  },
})

const allFields = computed(() => [
  {
    section: 'section 1',
    fields: [
      {
        label: 'شناسه فراگیر',
        name: 'name',
        type: 'data',
        readonly: true,
      },
      {
        label: 'تاریخ عضویت',
        name: 'joining_date',
        type: 'data',
        readonly: true,
      },
      {
        label: 'نشانی رایانامه',
        name: 'email_id',
        type: 'data',
        readonly: true,
      },
    ],
  },
  {
    section: 'section 2',
    fields: [
      {
        label: 'نام',
        name: 'first_name',
        type: 'data',
        readonly: props.editMode,
      },
      {
        label: 'نام میانی',
        name: 'middle_name',
        type: 'data',
        readonly: props.editMode,
      },
      {
        label: 'نام خانوادگی',
        name: 'last_name',
        type: 'data',
        readonly: props.editMode,
      },
    ],
  },
  {
    section: 'section 3',
    fields: [
      {
        label: 'شماره تلفن همراه',
        name: 'student_mobile_number',
        type: 'data',
        readonly: props.editMode,
      },
      {
        label: 'تاریخ تولد',
        name: 'date_of_birth',
        type: 'data',
        readonly: props.editMode,
      },
      {
        label: 'جنسیت',
        name: 'gender',
        type: 'data',
        readonly: props.editMode,
      },
    ],
  },
  {
    section: 'section 4',
    fields: [
      {
        label: 'گروه خونی',
        name: 'blood_group',
        type: 'data',
        readonly: props.editMode,
      },
      {
        label: 'ملیت',
        name: 'nationality',
        type: 'data',
        readonly: props.editMode,
      },
    ],
  },
])
</script>
