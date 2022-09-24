// Alert conditional inputs

const hiddenClass = 'input-hidden';
const trigger = document.querySelector('#alertTimeTrigger');

if (trigger) {
    const frequencyInput = trigger.querySelector('#frequency');
    const row = document.querySelector('#alertTimeRow');

    const hourDiv = row.querySelector('#hour').parentElement;
    const weekdayDiv = row.querySelector('#weekday').parentElement;
    const dayDiv = row.querySelector('#day').parentElement;

    // Hide fields based on field value on load
    const frequency = frequencyInput.value;
    if (frequency == 'h') {
        hourDiv.classList.add(hiddenClass)
        weekdayDiv.classList.add(hiddenClass)
        dayDiv.classList.add(hiddenClass)
    } else if (frequency == 'd') {
        weekdayDiv.classList.add(hiddenClass)
        dayDiv.classList.add(hiddenClass)
    } else if (frequency == 'w') {
        dayDiv.classList.add(hiddenClass)
    } else if (frequency == 'm') {
        weekdayDiv.classList.add(hiddenClass)
    }

    // Update fields visibility when frequency changes

    frequencyInput.addEventListener('change', function () {
        const frequency = this.value;
        // Display fields conditionaly
        if (frequency == 'h') {
            hourDiv.classList.add(hiddenClass)
            weekdayDiv.classList.add(hiddenClass)
            dayDiv.classList.add(hiddenClass)
        } else if (frequency == 'd') {
            hourDiv.classList.remove(hiddenClass)
            weekdayDiv.classList.add(hiddenClass)
            dayDiv.classList.add(hiddenClass)
        } else if (frequency == 'w') {
            hourDiv.classList.remove(hiddenClass)
            weekdayDiv.classList.remove(hiddenClass)
            dayDiv.classList.add(hiddenClass)
        } else if (frequency == 'm') {
            hourDiv.classList.remove(hiddenClass)
            weekdayDiv.classList.add(hiddenClass)
            dayDiv.classList.remove(hiddenClass)
        }
    });

}

