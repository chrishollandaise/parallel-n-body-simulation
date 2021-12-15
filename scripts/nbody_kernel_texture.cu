__constant__ double g;
__constant__ double time_step;
__constant__ double particle_count;

extern "C" {

__global__ void update_velocity( double * const __restrict__ mass, double *x , double *y , double *z , double *v_x , double *v_y , double *v_z ) {
    int i = blockIdx.x * blockDim.x + threadIdx.x;
    if( i < particle_count ) {
        double local_mass = mass[i];

        // Do force, acceleration, velocity, and movement effects for each particle
        for ( int j = 0 ; j < particle_count - 1 ; j++) {
            if( i != j ) {
                // Calculate total distance from two particles
                double dist = sqrt( pow( (double)(x[i] - x[j]) , (double)2 ) + pow( (double)(y[i] - y[j]) , (double)2 ) + pow( (double)(z[i] - z[j]) , (double)2 ) );

                // Calculate net force on two particles
                double net_force = ( ( local_mass * mass[j] ) / pow( dist , (double)2 ) ) * g;

                // Compute each force vector
                double f_x = net_force * ( ( x[j] - x[i] ) / dist );
                double f_y = net_force * ( ( y[j] - y[i] ) / dist );
                double f_z = net_force * ( ( z[j] - z[i] ) / dist );

                // Calculate new velocity with decay in consideration plus new acceleration relative to time_step
                v_x[i] = v_x[i] + ( f_x / local_mass ) * time_step;
                v_y[i] = v_y[i] + ( f_y / local_mass ) * time_step;
                v_z[i] = v_z[i] + ( f_z / local_mass ) * time_step;
            }
        }
    }
}

__global__ void update_position( double *x , double *y , double *z , double *v_x , double *v_y , double *v_z ) {
    int i = blockIdx.x * blockDim.x + threadIdx.x;
    // Update each coordinate location with current velocity in consideration over the span of a time time_step
    if ( i < particle_count ) {
        x[i] = x[i] + v_x[i] * time_step;
        y[i] = y[i] + v_y[i] * time_step;
        z[i] = z[i] + v_z[i] * time_step;
    }
}

}