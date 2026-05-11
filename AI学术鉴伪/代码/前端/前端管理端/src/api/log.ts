import http from './request'

export default {
  getLogs(params: any) {
    return http.get('/user_action_log/', { params });
  },

  getLogStatistics(params: { days?: number }) {
    return http.get('/user_action_log/statistics/', { params });
  },

  deleteLog(logId: number) {
    return http.delete(`/user_action_log/${logId}/`);
  },

  getLogDetail(logId: number) {
    return http.get(`/user_action_log/${logId}/detail/`);
  },

  markAnomaly(logId: number, isAnomaly: boolean) {
    return http.put(`/user_action_log/${logId}/mark_anomaly/`, {
      is_anomaly: isAnomaly,
    });
  },

  downloadLogs(params: {
    query?: number[];
    status?: string;
    operation_type?: string;
    startTime?: string;
    endTime?: string;
  }) {
    return http.get('/user_action_log/download/', { 
      params: {
        ...params,
        query: params.query?.join(',')
      },
      responseType: 'blob'
    });
  }
} 
