<template>
  <v-container>
    <v-row>
      <!-- Card for Statistics -->
      <v-col cols="12" md="6">
        <v-card class="mx-auto pa-4" max-height="75vh" elevation="10" flat>
          <v-card-title>STATS</v-card-title>
          <v-card-text>
            <v-row>
              <v-col cols="12">
                <p class="stat total">Total Applications: {{ totalApps }}</p>
                <p class="stat applied">
                  Total Applied: {{ appliedCount }} ({{ appliedPercent }}%)
                </p>
                <p class="stat interview">
                  Total Interviewing: {{ interviewingCount }} ({{
                    interviewingPercent
                  }}%)
                </p>
                <p class="stat rejected">
                  Total Rejected: {{ rejectedCount }} ({{ rejectedPercent }}%)
                </p>
                <p class="stat ghosted">
                  Total Ghosted: {{ ghostedCount }} ({{ ghostedPercent }}%)
                </p>
                <p class="stat offer">
                  Total Offers: {{ offerCount }} ({{ offerPercent }}%)
                </p>
              </v-col>
            </v-row>
          </v-card-text>
        </v-card>
      </v-col>

      <!-- Card for Chart -->
      <v-col cols="12" md="6">
        <v-card class="mx-auto pa-4" elevation="10" flat>
          <v-card-title>App Status Distribution</v-card-title>
          <v-card-text>
            <div id="chart" style="height: 300px"></div>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script lang="ts">
import { defineComponent, ref, onMounted } from "vue";
import axios from "axios";
import * as echarts from "echarts";

export default defineComponent({
  name: "StatsPage",
  setup() {
    const totalApps = ref(0);
    const appliedCount = ref(0);
    const interviewingCount = ref(0);
    const rejectedCount = ref(0);
    const ghostedCount = ref(0);
    const offerCount = ref(0);

    const appliedPercent = ref(0);
    const interviewingPercent = ref(0);
    const rejectedPercent = ref(0);
    const ghostedPercent = ref(0);
    const offerPercent = ref(0);

    const fetchStats = async () => {
      try {
        const response = await axios.get("http://127.0.0.1:8000/applications/");

        const apps = response.data;
        console.log("app count:", apps[1]);
        totalApps.value = apps.length;

        appliedCount.value = apps.filter(
          (app: { status: string }) => app.status === "Applied"
        ).length;
        interviewingCount.value = apps.filter(
          (app: { status: string }) => app.status === "Interviewing"
        ).length;
        rejectedCount.value = apps.filter(
          (app: { status: string }) => app.status === "Rejected"
        ).length;
        offerCount.value = apps.filter(
          (app: { status: string }) => app.status === "Offer"
        ).length;
        ghostedCount.value = apps.filter(
          (app: { status: string }) => app.status === "Ghosted"
        ).length;

        appliedPercent.value = Number(
          ((appliedCount.value / totalApps.value) * 100).toFixed(1)
        );
        interviewingPercent.value = Number(
          ((appliedCount.value / totalApps.value) * 100).toFixed(1)
        );
        rejectedPercent.value = Number(
          ((appliedCount.value / totalApps.value) * 100).toFixed(1)
        );
        ghostedPercent.value = Number(
          ((appliedCount.value / totalApps.value) * 100).toFixed(1)
        );
        offerPercent.value = Number(
          ((appliedCount.value / totalApps.value) * 100).toFixed(1)
        );

        console.log("total count:", totalApps);
        console.log("applied count:", appliedCount);
        console.log("interview count:", interviewingCount);
        console.log("rejected count:", rejectedCount);
        console.log("ghosted count:", ghostedCount);
        console.log("offer count:", offerCount);

        renderChart();
      } catch (error) {
        console.error("Error fetching statistics: ", error);
      }
    };

    const renderChart = () => {
      const chartDom = document.getElementById("chart");
      const pieChart = echarts.init(chartDom);
      const option = {
        title: {
          text: "App Status Distribution",
          left: "center",
        },
        tooltip: {
          trigger: "item",
        },
        legend: {
          bottom: "5%",
          left: "center",
        },
        series: [
          {
            name: "Applications",
            type: "pie",
            radius: "50%",
            data: [
              { value: appliedCount.value, name: "Applied" },
              { value: interviewingCount.value, name: "Interviewing" },
              { value: rejectedCount.value, name: "Rejected" },
              { value: ghostedCount.value, name: "Ghosted" },
              { value: offerCount.value, name: "Offer" },
            ],
            emphasis: {
              itemStyle: {
                shadowBlur: 10,
                shadowOffsetX: 0,
                shadowColor: "rgba(0,0,0, 0.5)",
              },
            },
          },
        ],
      };
      pieChart.setOption(option);
    };
    onMounted(fetchStats);
    return {
      totalApps,
      appliedCount,
      appliedPercent,
      interviewingCount,
      interviewingPercent,
      rejectedCount,
      rejectedPercent,
      ghostedCount,
      ghostedPercent,
      offerCount,
      offerPercent,
    };
  },
});
</script>

<style scoped>
/* Custom Styling for Paragraphs */
.stat {
  font-size: 32px; /* Adjust font size */
  font-weight: 500; /* Medium weight */
  margin: 8px 0; /* Space between items */
  color: #333; /* Text color */
  padding-left: 10px; /* Add some padding for alignment */
  background-color: #f5f5f5; /* Light background */
  border-radius: 4px; /* Slightly rounded corners */
}
.total {
  border-left: 4px solid #636363;
}
.applied {
  border-left: 4px solid #4359b9; /* Add a left border for emphasis */
}

.interview {
  border-left: 4px solid #7fc162; /* Add a left border for emphasis */
}

.rejected {
  border-left: 4px solid #f7be47; /* Add a left border for emphasis */
}
.ghosted {
  border-left: 4px solid #e84f54; /* Add a left border for emphasis */
}
.offer {
  border-left: 4px solid #62b3d6; /* Add a left border for emphasis */
}
</style>
