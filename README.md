# Photographer Scheduler

A scheduling application built using Python. Checks the availability of each photographer on each day, and assigns teams to events on days they are available.

Completed features:
 * Create lists per day of photographers that are available.

To be completed:
 * Create lists of events per day.
 * Assign photographers to events based on experience level, availability, and location.
 * Implement read + write functionality to and from xslx file.

 # How It Works
 * CSV of photographer availability is iterated on by date, creating lists based on location of photographers
    * Lists contain photographer name and experience level
 * CSV of events is separated into lists of events based on their date 
    *List contains event name, number of needed photographers, and start/end times
 * One captain photographer is assigned to each event, remainder of team is generated depending on the number of needed photographers.
    * If no photographers of the needed level are available, a higher level photographer will be placed in that role. If no photographers are available, a placeholder "Photographer level X or higher needed" is used.