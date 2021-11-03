Title: River monitoring with Datadog
Date: 2021-11-02
Category: monitoring
Description: How I used my day-to-way tools to setup reliable monitoring on the river I live close by. 
Summary: Last month, Ardèche experienced _very_ heavy precipitations in the span of couple of hours. As a result, the dam located upriver from me opened the floodgates (literally), which caused the Chassezac level to raise by about 6.5m in about 1.5h. I've setup some monitoring using Datadog and Pagerduty to make sure I know about it as soon as possible.
Image: https://balthazar-rouberol-blog.s3.eu-west-3.amazonaws.com/river-monitoring/gravieres.webp
Tags: datadog
Keywords: weather, monitoring, datadog

<p style="text-align:center;font-style:italic;font-size:0.8em;">water level (m) over time</p>

Last month, Ardèche experienced _very_ heavy precipitations in the span of couple of hours. As a result, the dam located upriver from me opened the floodgates (literally), which caused the Chassezac level to raise by about 6.5m in about 1.5h. My basement was completely flooded, and the water level stabilized just about a 1m from the house ground floor. We had just enough time to move our belongings to the first floor. The riverside was unrecognizable, to the point where we found fish in the trees.

3 weeks later, the same thing happened, but this time the dam manager did their job. They only let enough water to make the dam wasn't overrun, while keeping everyone safe downriver.

What really bothered me though, is that at no point were we alerted of anything by EDF (the company managing the grid). No text, to alert, nothing.

Datadog to the rescue.

Using custom scripts, I now measure the [river level](https://github.com/brouberol/infrastructure/blob/master/playbooks/roles/gallifrey/monitoring/files/monitor_rivers) at the station before and after my house. I also keep tabs on the [amount of rain](https://github.com/brouberol/infrastructure/blob/master/playbooks/roles/gallifrey/monitoring/templates/monitor_rain) measured at these stations, as well as the general alert level.

<a target="blank" href="https://p.datadoghq.com/sb/bc352bb82-c122f0855899cdbcc73f2ca478d6d7b6"><picture>
    <source srcset="https://balthazar-rouberol-blog.s3.eu-west-3.amazonaws.com/river-monitoring/river-monitoring-dark.webp"
    media="(prefers-color-scheme: dark)">
    <img class=dark src="https://balthazar-rouberol-blog.s3.eu-west-3.amazonaws.com/river-monitoring/river-monitoring-light.webp" />
</picture></a>

By "chance", the first flood stopped right before the house level, and the second one stopped right before the basement. By extrapolating just a bit, I'm now able to have a good idea of the impact of a flood by looking at the river level at the station upriver.

I thus created Datadog monitors over the [river level](https://github.com/brouberol/infrastructure/blob/0d4fa0ca629b852e2e3cbff2d7e2ea0701135371/terraform/datadog/monitors.tf#L217-L239) and the [alert level](https://github.com/brouberol/infrastructure/blob/0d4fa0ca629b852e2e3cbff2d7e2ea0701135371/terraform/datadog/monitors.tf#L193-L215), and I hooked them to a personal [Pagerduty](https://pagerduty.com) account, using their free tier.

I made sure to enable `Critical Alers for High Urgency` in the app settings, which enables Pagerduty to override my phone volume preference, to wake me up even if is is in silent mode.

Now, if the dam managers decide to open the gates during the night (it has happened), I'll know.

![pagerduty](https://balthazar-rouberol-blog.s3.eu-west-3.amazonaws.com/river-monitoring/pagerduty.webp)
