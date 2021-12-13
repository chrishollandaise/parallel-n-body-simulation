__constant__ unsigned int g;
__constant__ unsigned int time_step;
__constant__ unsigned int particle_count;

extern "C" {

__global__ void update_velocity( int *mass, float *x , float *y , float *z , float *v_x , float *v_y , float *v_z ) {
    unsigned int i = blockIdx.x * blockDim.x + threadIdx.x;
    if( i < particle_count ) {
        int local_mass = mass[i];

        // Do force, acceleration, velocity, and movement effects for each particle
        for ( int j = 0 ; j < particle_count - 1 ; j++) {
            if( i != j ) {
                // Calculate total distance from two particles
                float dist = sqrt( pow( (float)(x[i] - x[j]) , (float)2 ) + pow( (float)(y[i] - y[j]) , (float)2 ) + pow( (float)(z[i] - z[j]) , (float)2 ) );

                // Calculate net force on two particles
                float net_force = ( ( local_mass * mass[j] ) / pow( dist , (float)2 ) ) * g;

                // Compute each force vector
                float f_x = net_force * ( ( x[j] - x[i] ) / dist );
                float f_y = net_force * ( ( y[j] - y[i] ) / dist );
                float f_z = net_force * ( ( z[j] - z[i] ) / dist );

                // Calculate new velocity with decay in consideration plus new acceleration relative to time_step
                v_x[i] = v_x[i] + ( f_x / local_mass ) * time_step;
                v_y[i] = v_y[i] + ( f_y / local_mass ) * time_step;
                v_z[i] = v_z[i] + ( f_z / local_mass ) * time_step;
            }
        }
    }
}

__global__ void update_position( float *x , float *y , float *z , float *v_x , float *v_y , float *v_z ) {
    unsigned int i = blockIdx.x * blockDim.x + threadIdx.x;
    // Update each coordinate location with current velocity in consideration over the span of a time time_step
    if ( i < particle_count ) {
        x[i] = x[i] + v_x[i] * time_step;
        y[i] = y[i] + v_y[i] * time_step;
        z[i] = z[i] + v_z[i] * time_step;
    }
}

}